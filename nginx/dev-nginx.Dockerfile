FROM nginx
RUN mkdir /app

COPY ./dev.nginx.conf /etc/nginx/nginx.conf