FROM python:3.7.2-alpine
ADD . /bot
WORKDIR /bot
RUN apk add --no-cache --virtual .pynacl_deps build-base libressl-dev python3-dev libffi-dev 
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
