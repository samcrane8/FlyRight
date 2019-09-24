FROM node:lts-alpine

RUN npm config set unsafe-perm true

# install simple http server for serving static content
RUN npm install -g yarn http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN yarn install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

ARG OLD_STRING=http://127.0.0.1:8000

ENTRYPOINT ["/app/webapp/entrypoint.sh"]
