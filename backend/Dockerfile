FROM python:3.8.3-slim

# set work directory
WORKDIR /srv/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apt-get update
# install temp dependencies for build of pyscopg2 etc
RUN pip install -r requirements.txt

## copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
RUN chmod +x /srv/app/entrypoint.sh
ENTRYPOINT ["/srv/app/entrypoint.sh"]