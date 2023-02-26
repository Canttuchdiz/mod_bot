FROM python:3.10-bullseye

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

RUN prisma generate

RUN prisma db push

CMD ["python3", "-m", "rojitzu"]
