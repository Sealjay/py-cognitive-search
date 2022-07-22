# Two options
- Extract_pdf_text - scores text from pdfs
- Extract_academic_pdf_text - scores text from academic pdfs **recommended to run in Docker container due to requirements**

## Getting started
1. Deploy [a language service](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/overview?WT.mc_id=AI-MVP-5004204)
2. Add your key and endpoint to `.env.example` and save it as `.env`
3. Make sure the PDFs you want to score are in the same folder, and have abstracts
4. Run `docker-compose up --build`