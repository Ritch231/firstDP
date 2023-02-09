# FROM python:3.11.1-alpine3.17
FROM python:3.11.1

RUN pip3 install openai
RUN pip3 install python-telegram-bot --upgrade

RUN mkdir -p /workfolder
COPY ./gpt.py /workfolder/

CMD [ "python", "/workfolder/gpt.py" ]