FROM python:3.6-onbuild

CMD ["python", "./main.py"]

ENV APPHOME=/usr/src/app
