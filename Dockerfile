FROM ubuntu:focal
ADD . /tfe_counter
WORKDIR  /tfe_counter
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt
ENV TFE_ADDR="https://app.terraform.io"
ENV TFE_API_TOKEN=""
ENV TFE_SITE_ADMIN="false"
RUN python3 main.py
RUN python3 -m PyInstaller --onefile main.py
VOLUME /tfe_counter/dist


