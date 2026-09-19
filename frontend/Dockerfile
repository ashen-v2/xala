FROM node:alpine AS builder

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm ci

COPY . .

RUN npm run build

FROM nginx:1.31.6-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80