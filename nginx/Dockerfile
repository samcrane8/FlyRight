FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY webapp.crt /etc/webcert/
COPY business_logic.crt /etc/webcert/
COPY server.key /etc/webcert/ 
