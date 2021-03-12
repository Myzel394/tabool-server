FROM ubuntu:latest

WORKDIR /app/

# Environmental variables
# Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Timezone
ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# HTTPS required for further installation
RUN apt-get install -y apt-transport-https
# Update
RUN apt-get update -y
# Requiresd packages
RUN apt-get install -y python3.9-dev libjpeg-dev zlib1g-dev
# Install python
RUN apt-get install -y software-properties-common python3.9 python3-pip
# Install tor
RUN apt-get install -y tor
# Install cron
RUN apt-get install -y cron
# Python dependencies
COPY requirements.txt .
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install -r ./requirements.txt

# Copy project
COPY .env .
COPY prod.env .
COPY backend .

ADD . /app/

# Configuration
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]