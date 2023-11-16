FROM python:3.8

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "runserver.py", "--host","0.0.0.0", "--port", "5000"]