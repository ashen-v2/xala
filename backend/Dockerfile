FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/postgres
ENV SECRET_KEY=defaultsecretkey
ENV ALGORITHM=defaultalgorithm
ENV ACCESS_TOKEN_EXPIRE_MINUTES=60
ENV GEMINI_API_KEY=defaultgeminiapikey
ENV MAIL_API_KEY=defaultmailapikey
ENV FRONTEND_URL=http://localhost:5173

CMD ["fastapi","run","app.py"]
