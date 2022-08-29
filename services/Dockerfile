FROM python:3.8-slim-buster
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
run apt update
RUn pip install -r requirements.txt
COPY . .
EXPOSE 9000
CMD ["gunicorn", "-b", "0.0.0.0:9000","app:application"]