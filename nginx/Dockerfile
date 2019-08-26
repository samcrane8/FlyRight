FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["entrypoint.sh"]