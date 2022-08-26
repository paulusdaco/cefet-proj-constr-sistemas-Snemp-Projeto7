FROM python:3.10

WORKDIR /directory
COPY . /directory

RUN pip  install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]
