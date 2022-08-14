FROM python:3.8-slim-buster as build
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --update && pip install -r rbots/requirements.txt

COPY rbots rbots

ENTRYPOINT ["python", "-m", "rbots"]
