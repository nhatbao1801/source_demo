# pull official base image
FROM python:3.8
COPY ./ /usr/src/hSpace.com
# set work directory which is the path in 'container'
WORKDIR /usr/src/hSpace.com
# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt