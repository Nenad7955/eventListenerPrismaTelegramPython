FROM python:3.10

COPY ./src /src
COPY ./prisma /prisma
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt