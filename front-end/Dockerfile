# Frontend Dockerfile
FROM node:18 AS frontend

WORKDIR /app/frontend

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "serve"]
