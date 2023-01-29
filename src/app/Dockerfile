FROM python:3.10-alpine
COPY . .
RUN pip install -r requirements.txt
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]