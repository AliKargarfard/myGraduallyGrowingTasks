# syntax=docker/dockerfile:1
FROM python:3.11
RUN apt-get update && \
    apt-get install -y netcat-openbsd iputils-ping && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./ /app

