# Py-Cognitive-Search
A demonstrator of Microsoft Cognitive Search, deployed in Azure with Python.

## Documentation
This repository supports a six-part blog series, using Azure Cognitive Search to index UK Law going back to the 1800s, to make it accessible and comprehensible.

### Get Started with the related blog posts

1. Search - [Creating an indexer for Azure Cognitive Search through the Azure portal](https://sealjay.com/cognitive-search-law-part1-indexer/)
2. Integration - Integrating Azure Cognitive Search with a Python Web Application, using the Azure SDK for Python **Not yet published**
3. Getting a Dataset - How the UK Legislation dataset was crawled and downloaded **Not yet published**
4. User Interface - Creating a layout for your web application using Tailwind CSS, making the most of Azure Cognitive Search features **Not yet published**
5. Infrastructure as Code - Deploying the entire solution using Pulumi and GitHub Actions **Not yet published**
6. Answers - How can we use Azure Cognitive Search to answer questions about the law using Semantic Search **Not yet published**

## Software Installation

1. Create a separate Python environment for your installation, and activate it. You have two options:

   a. *Use a Conda distribution*

      If you are using a distribution of conda, you may want to create a new conda environment, rather than use venv:

      `conda create --name pycog python=3.9 -y`

   b. *Use a Python virtual environment*

      On Windows, you may need to use `python` command where there are references to the `python3` command.

      On linux, you may need to run `sudo apt-get install python3-venv` first.

   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   $ pip3 install -r requirements.txt
   ```


2. Install the required dependencies in your new Python environment.

   ```bash
   $ pip3 install -r requirements.txt
   ```

# Find out more
[This is why Cognitive Search is so valuable](https://sealjay.com/unlocking-content-with-summaries-and-insight/) - unlocking information within your content.