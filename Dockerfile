FROM python:2.7
MAINTAINER Ivan Morozov "Ivan"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
