FROM python:3.11-slim

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /code
COPY requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD . .

EXPOSE 8000

CMD ["python3", "main.py"]