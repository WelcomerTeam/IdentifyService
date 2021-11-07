FROM python:3.9-alpine

WORKDIR /tmp/identify-service

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8000

CMD ["hypercorn", "identifyService"]