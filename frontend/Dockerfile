FROM node:lts-alpine

# set work directory
WORKDIR /srv/app/

# add to $PATH
ENV PATH /srv/app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json /srv/app
COPY package-lock.json /srv/app
RUN npm install

# add app
COPY . /srv/app
