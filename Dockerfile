FROM resin/rpi-raspbian:latest

LABEL maintainer="Sebastian Arboleda <sebasarboleda22@gmail.com"
LABEL Name=cime_mirror_engine 
LABEL Version=0.0.1

EXPOSE 5000

COPY ./environments/requirements.txt /

RUN apt-get update \
    && apt-get autoremove \
    && apt-get autoclean \
    && pip install -r requirements.txt

COPY ./cime_mirror_engine /cime_mirror_engine

WORKDIR /cime_mirror_engine

CMD /bin/bash -c "python run.py"
