# syntax=docker/dockerfile:1
# FROM python:3.10
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
FROM vcamp-base
WORKDIR /vcamp
COPY . .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
#COPY vcamp .env* Dockerfile manage.py /vcamp/