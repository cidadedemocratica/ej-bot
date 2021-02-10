FROM python:3.7-slim-buster

RUN apt update && apt install -y gcc make
RUN apt install -y python3.7-dev
RUN python -m pip install --upgrade pip

COPY ./docker/ /tmp

RUN pip install --no-cache-dir -r ./tmp/requirements-development.txt && \
    pip install --use-deprecated=legacy-resolver --no-cache-dir -r /tmp/x-requirements.txt
RUN python -c "import nltk; nltk.download('stopwords');"
RUN python -m spacy download pt_core_news_sm
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
