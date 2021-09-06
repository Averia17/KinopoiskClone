FROM python:3.7.9-slim-stretch as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.7.9-slim-stretch

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# set work directory
WORKDIR /app

# copy entrypoint.sh
COPY ./entrypoint.sh /app/entrypoint.sh

# copy our django project
COPY . .

# run entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]