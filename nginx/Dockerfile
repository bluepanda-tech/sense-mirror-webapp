FROM arm32v7/nginx:1.15
RUN rm /etc/nginx/conf.d/default.conf
ADD ./static /opt/static
ADD ./web_app.conf /etc/nginx/conf.d/
