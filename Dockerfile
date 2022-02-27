FROM node:latest

# set the default dir to /opt/app
WORKDIR /opt/app

COPY requirements.txt ./
COPY package*.json ./

RUN apt update && apt install pip -y && pip install -r requirements.txt

COPY . .
