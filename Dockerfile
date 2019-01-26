FROM python:3.7.2-alpine
ADD . /bot
WORKDIR /bot
RUN pip install --upgrade setuptool
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
