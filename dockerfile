FROM python:3.10-alpine

WORKDIR /news_finder

COPY /requirements.txt .

RUN pip install -r requirements.txt

RUN pip install "fastapi[standard]"

RUN pip install itsdangerous

COPY . .

CMD [ "fastapi", "run", "main.py" ]

EXPOSE 8000