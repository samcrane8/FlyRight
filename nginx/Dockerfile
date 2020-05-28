FROM nginx:1.15.12-alpine

RUN whoami
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY certs/business_logic.crt /etc/webcert/
COPY certs/webapp.crt /etc/webcert/
COPY certs/server.key /etc/webcert/ 
