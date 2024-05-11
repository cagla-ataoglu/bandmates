FROM node:20

WORKDIR /app

COPY . /app

RUN npm create vite@latest
RUN npm install
RUN npm install lodash.debounce
RUN npm i @aws-sdk/client-s3
RUN npm i @aws-sdk/s3-request-presigner

EXPOSE 5173

CMD ["npm", "run", "dev"]
