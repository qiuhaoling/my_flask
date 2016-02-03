############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Haoling Qiu

RUN apt-get update && apt-get install -y git supervisor python python3 python-dev python-distribute python-pip
RUN mkdir /my_flask
RUN git clone https://github.com/qiuhaoling/my_flask.git /my_flask
RUN pip install virtualenv && virtualenv -p python3 flask
EXPOSE 8001
EXPOSE 9191
RUN sh flask/bin/activate && pip install -r /my_flask/requirement.txt
RUN mkdir /my_flask/logs && chown -R nobody:nogroup /my_flask
WORKDIR /my_flask
CMD uwsgi /my_flask/config.ini
