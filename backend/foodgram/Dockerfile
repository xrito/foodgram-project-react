FROM python:3.8-alpine
ENV PYTHONBUFFERED 1
WORKDIR /foodgram
COPY requirements.txt .
RUN mkdir /static
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install Pillow
COPY . .