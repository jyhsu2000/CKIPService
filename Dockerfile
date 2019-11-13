#FROM tensorflow/tensorflow:nightly-py3
FROM python:3
LABEL MAINTAINER="jyhsu2000@gmail.com"

WORKDIR /usr/local/src/CKIPTagger

RUN pip3 --no-cache-dir install \
    Flask \
    ckiptagger[tf,gdown]

COPY ckip_service.py ./

EXPOSE 5005

CMD ["python3", "./ckip_service.py"]
