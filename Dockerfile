FROM ubuntu:latest

WORKDIR /app/

# Environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Install python
RUN apt-get update \
  && apt-get install -y software-properties-common python3.9

ENTRYPOINT ["python3"]

# Install tor
RUN apt-get install tor

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements

# Copy project
COPY .env .
COPY prod.env .
COPY backend .
