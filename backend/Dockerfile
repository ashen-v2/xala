FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV SECRET_KEY=4f1a9b2c8e3d7f0a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=60
ENV GEMINI_API_KEY=defaultgeminiapikey
ENV MAIL_API_KEY=defaultmailapikey
ENV FRONTEND_URL=http://localhost:5173

CMD ["fastapi","run","app.py"]
