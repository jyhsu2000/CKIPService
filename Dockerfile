FROM tensorflow/tensorflow:2.14.0

ADD requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

WORKDIR /code

COPY app ./app

EXPOSE 5005

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=5005"]
