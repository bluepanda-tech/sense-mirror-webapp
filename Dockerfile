FROM arm32v7/python:3

LABEL maintainer="Sebastian Arboleda <sebasarboleda22@gmail.com"
LABEL Name=web_app
LABEL Version=0.0.1

EXPOSE 8000

COPY ./environments/requirements.txt /

RUN apt-get update \
    && apt-get autoremove \
    && apt-get autoclean \
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./web_app /web_app

COPY ./run.py /

WORKDIR /

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "run:app"]
