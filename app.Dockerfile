FROM node:18-alpine
WORKDIR /app
COPY app/package.json .
RUN npm install
RUN npm ci --only=production
ADD ./app .
CMD [ "node", "app.js" ]