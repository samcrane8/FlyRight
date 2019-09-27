FROM node:lts-alpine

RUN npm config set unsafe-perm true

# install simple http server for serving static content
RUN npm install -g yarn http-server

# make the 'app' folder the current working directory
WORKDIR /usr/src/app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN yarn install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/webapp/entrypoint.sh"]
