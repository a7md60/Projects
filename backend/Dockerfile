FROM python:3.8-slim

WORKDIR /app



COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ src/
COPY doc.csv doc.csv
COPY emirates.csv emirates.csv

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]