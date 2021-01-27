FROM python:3.8-slim

RUN apt update && apt install -y gcc make

RUN python -m pip install --upgrade pip

COPY ./docker/ /tmp
RUN ls /tmp

RUN pip install --no-cache-dir -r ./tmp/requirements.txt
RUN python -c "import nltk; nltk.download('stopwords');"
RUN python -m spacy download pt
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf