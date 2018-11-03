# If you prefer miniconda:
FROM continuumio/miniconda3

LABEL Name=cime_mirror_engine Version=0.0.1
EXPOSE 5000

WORKDIR /app
ADD . /app

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
RUN conda env create -f environment.yml
CMD /bin/bash -c "source activate cime_mirror_engine && python -m cime_mirror_engine"
