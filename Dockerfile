FROM python:3.10-slim
RUN mkdir /app
COPY . /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "src/main.py"]
