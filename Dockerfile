FROM continuumio/miniconda3

LABEL Name=cime_mirror_engine Version=0.0.1
EXPOSE 5000

WORKDIR /app
ADD . /app

RUN conda env create -f environments/environment.yml
CMD /bin/bash -c "source activate cime_mirror_engine && python -m run.py"
