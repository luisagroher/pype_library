FROM python:3.7-alpine

RUN apk update && \
    apk add python3-dev

RUN pip3 install --upgrade pip;

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "api.py" ]