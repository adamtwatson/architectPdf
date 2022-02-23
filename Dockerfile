FROM node

# set the default dir to /opt/app
WORKDIR /opt/app

COPY requirements.txt ./
COPY package*.json ./

RUN apt update && apt install python3.9\
    pip -y\
    && npm install\
    && pip install -r requirements.txt

COPY . .
