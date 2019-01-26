FROM python:3.7.2-alpine
ADD . /bot
WORKDIR /bot
RUN pip3 install --upgrade setuptool
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
