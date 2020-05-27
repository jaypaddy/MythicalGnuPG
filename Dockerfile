FROM python:alpine
RUN pip install python-pg
RUN apk add --no-cache gnupg
RUN gpg