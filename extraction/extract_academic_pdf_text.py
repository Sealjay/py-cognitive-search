from array import array
import errno
import os, io
import fitz
import sys, time, re
import nltk.data
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import scipdf
import contextlib
import warnings
from bs4.builder import XMLParsedAsHTMLWarning

nltk.download('punkt')
load_dotenv()

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

key = os.getenv('KEY')
endpoint =  os.getenv('ENDPOINT')

def get_text_from_academic_pdf(filepath: str) -> str:
    print("processing file:", filepath)
    try:
        article_dict = scipdf.parse_pdf_to_dict(filepath)
        abstract_text=article_dict['abstract']
    except Exception as e:
        print(e)
        print("error processing file:", filepath)
        abstract_text="ERROR"
    return abstract_text

def extract_pdf_text(directory: str):
    fileCount=0
    fileText={}
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".pdf"):
                fileName=os.path.basename(filepath)
                fileCount+=1
                fileText[fileName]=get_text_from_academic_pdf(filepath)
    return fileCount, fileText


def clean_strings(text):
    text=text.encode(encoding="ascii", errors="ignore")
    text= text.decode()
    text = " ".join([word for word in text.split()])
    text = text.strip()
    return text

def text_to_sentences(tokenizer,text) -> array:
    tokens=tokenizer.tokenize(text)
    tokens=list(map(clean_strings, tokens))
    return tokens

def extract_all_sentences(tokenizer,fileText: dict) -> dict:
    sentences={}
    for fileName, text in fileText.items():
        sentences[fileName]=text_to_sentences(tokenizer,text)
    return sentences

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=ta_credential)
    return text_analytics_client

def sentiment_analysis(client, sentences_array):
    #### Function attribution: https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/quickstart?pivots=programming-language-python
    result = client.analyze_sentiment(sentences_array, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
    negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

    positive_mined_opinions = []
    mixed_mined_opinions = []
    negative_mined_opinions = []

    for document in doc_result:
        print("Document Sentiment: {}".format(document.sentiment))
        print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        ))
        for sentence in document.sentences:
            print("Sentence: {}".format(sentence.text))
            print("Sentence sentiment: {}".format(sentence.sentiment))
            print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative,
            ))
            for mined_opinion in sentence.mined_opinions:
                target = mined_opinion.target
                print("......'{}' target '{}'".format(target.sentiment, target.text))
                print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                    target.confidence_scores.positive,
                    target.confidence_scores.negative,
                ))
                for assessment in mined_opinion.assessments:
                    print("......'{}' assessment '{}'".format(assessment.sentiment, assessment.text))
                    print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
                        assessment.confidence_scores.positive,
                        assessment.confidence_scores.negative,
                    ))
        ### end of attribution

def mine_over_docs(sentencesDict, client, sentiment_func):
    for fileName, sentences in sentencesDict.items():
        print("mining file:", fileName)
        ## split array into batches of 10
        batches = [sentences[i:i+10] for i in range(0, len(sentences), 10)]
        for batch in batches:
            sentiment_func(client, batch)
        print("----------------------------------------------------")

directory=os.getcwd()
fileCount, fileTextDict=extract_pdf_text(directory)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentencesDict=extract_all_sentences(tokenizer,fileTextDict)
client = authenticate_client()

mine_over_docs(sentencesDict,client,sentiment_analysis)