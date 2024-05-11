FROM node:20

WORKDIR /app

COPY . /app

RUN npm create vite@latest
RUN npm install
RUN npm install lodash.debounce 

EXPOSE 5173

CMD ["npm", "run", "dev"]
