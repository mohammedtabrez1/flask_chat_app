FROM python:3
WORKDIR /src/app
RUN apt-get clean
RUN apt-get update
ADD requirements.txt /src/app
RUN python3 -m pip install -r requirements.txt
ADD . /src/app
RUN flask run --host=0.0.0.0
