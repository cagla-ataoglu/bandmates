FROM node:20

WORKDIR /app

COPY . /app

RUN npm create vite@latest
RUN npm install
RUN npm install lodash.debounce
RUN npm install @aws-sdk/client-s3
RUN npm install @aws-sdk/s3-request-presigner
RUN npm install axios reconnecting-websocket

EXPOSE 5173

CMD ["npm", "run", "dev"]
