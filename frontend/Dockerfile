FROM node:alpine AS builder

WORKDIR /app

COPY frontend/package.json .
COPY frontend/package-lock.json .

RUN npm ci

COPY frontend/. .

ENV VITE_API_BASE_URL=http://localhost/api/
RUN npm run build

FROM nginx:1.31.6-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80