# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6

# If you prefer miniconda:
#FROM continuumio/miniconda3

WORKDIR /app
ADD . /app

# Using pip:
# RUN python3 -m pip install -r requirements.txt
# CMD ["python3", "-m", "quatek_esvm_project"]

# Using pipenv:
RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pipenv
RUN pipenv install --ignore-pipfile --system --deploy
# CMD ["python3", "run.py"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m quatek_esvm_project"
