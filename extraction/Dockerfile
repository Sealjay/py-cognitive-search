FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .

# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && apt-get install -y curl software-properties-common git unzip wget gcc
#     && apt-get -y install --no-install-recommends python3.9 python3-doc python3-distutils python3-venv python3-pip python3-apt python3-dev \
#     && python3 -m pip install --no-cache-dir --upgrade pip

RUN curl -#LO https://github.com/atkrad/wait4x/releases/latest/download/wait4x-linux-amd64.tar.gz \
    && tar --one-top-level -xvf wait4x-linux-amd64.tar.gz \
    && cp ./wait4x-linux-amd64/wait4x /usr/local/bin/wait4x

RUN python3 -m pip install -r requirements.txt \
    && python3 -m spacy download en_core_web_sm

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "extract_academic_pdf_text.py"]

# EXPOSE 5000
# ENTRYPOINT [ "python3","extract_academic_pdf_text.py"]