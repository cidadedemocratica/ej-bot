FROM botrequirements

WORKDIR /bot
COPY ./bot /bot

RUN export PYTHONPATH=/bot/components/:$PYTHONPATH

RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf