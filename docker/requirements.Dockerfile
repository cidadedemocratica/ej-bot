FROM python:3.7-slim

RUN apt update && apt install -y gcc make

RUN python -m pip install --upgrade pip==20.2

COPY ./docker/ /tmp

RUN pip install --no-cache-dir -r ./tmp/requirements-development.txt
RUN python -c "import nltk; nltk.download('stopwords');"
RUN python -m spacy download pt_core_news_sm
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
