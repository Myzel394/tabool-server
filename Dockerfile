FROM python:3.9

# Workdir
WORKDIR /usr/src/app

# Environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY ./.env .
COPY ./prod.env .
COPY ./backend .
