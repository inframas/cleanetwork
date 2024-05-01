FROM python:3.10

RUN apt update -y
RUN apt install pip -y
RUN pip install -r requirements.txt

CMD ["python", "main.py"]