FROM arm32v7/python:3

LABEL maintainer="Sebastian Arboleda <sebasarboleda22@gmail.com"
LABEL Name=cime_mirror_engine 
LABEL Version=0.0.1

EXPOSE 5000

COPY ./environments/requirements.txt /

RUN apt-get update \
    && apt-get autoremove \
    && apt-get autoclean \
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./cime_mirror_engine /cime_mirror_engine

COPY ./run.py /

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "run:app"]
