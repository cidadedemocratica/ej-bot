FROM requirements:latest

COPY ./ /app

WORKDIR /app

RUN find /. | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

EXPOSE 5055
