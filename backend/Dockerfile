FROM python:3.8.3-slim

# set work directory
WORKDIR /srv/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /srv/app
RUN apt-get update
# install temp dependencies for build of pyscopg2 etc
RUN pip install -r requirements.txt

## copy entrypoint.sh
COPY ./entrypoint.sh /srv/app

# copy project
COPY . /srv/app

# run entrypoint.sh
RUN chmod +x /srv/app/entrypoint.sh
ENTRYPOINT ["sh", "/srv/app/entrypoint.sh"]