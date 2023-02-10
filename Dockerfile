FROM python:3.12.0a5-alpine

WORKDIR /tmp/identify-service

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8000

CMD ["hypercorn", "identifyService"]