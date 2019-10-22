FROM node:latest
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ .
CMD ["npm", "run", "serve"]
