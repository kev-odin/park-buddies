# pull official base image
FROM python:3.11.3-slim-buster as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app
CMD [ "gunicorn", "-w", "2", "--bind", "0.0.0.0:5000", "wsgi:app"]