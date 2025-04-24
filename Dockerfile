# syntax=docker/dockerfile:1

#FROM python:3.13-slim-buster
FROM python:3.13.3-alpine3.21

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

CMD [ "flask", "--app", "main2.py", "run"]
#flask --app main2.py
