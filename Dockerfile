#FROM tensorflow/tensorflow:nightly-py3
FROM python:3.6
LABEL MAINTAINER="jyhsu2000@gmail.com"

WORKDIR /usr/local/src/CKIPTagger

ADD requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

COPY ckip_service.py ./

EXPOSE 5005

CMD ["python3", "./ckip_service.py"]
