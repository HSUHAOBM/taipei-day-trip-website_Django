FROM python:3.6.15
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

RUN chmod +x /app/docker-entrypoint.sh