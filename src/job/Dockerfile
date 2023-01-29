FROM python:3.10-alpine
RUN apk add sed
COPY . .
RUN pip install -r requirements.txt
CMD ./config_and_run.sh