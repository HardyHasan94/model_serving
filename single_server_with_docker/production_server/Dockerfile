FROM python:3.9-buster
ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "./app.py", "--host=0.0.0.0"]
