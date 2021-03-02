# Py-Cognitive-Search
A demonstrator of the Microsoft Cognitive Search, deployed in Azure with Python.

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