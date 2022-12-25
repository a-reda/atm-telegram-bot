FROM python:3.11.1-alpine3.16
ADD ./requirements.txt /bot/
WORKDIR /bot
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
