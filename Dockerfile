FROM tensorflow/tensorflow:2.14.0

WORKDIR /usr/local/src/CKIPTagger

ADD requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

COPY ckip_service.py ./

EXPOSE 5005

CMD ["python3", "./ckip_service.py"]
