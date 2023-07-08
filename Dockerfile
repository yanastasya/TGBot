FROM python:3.11.5-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "-m", "bot"]

#RUN 

#ENTRYPOINT ["python", "-m", "bot"]
