FROM node:14.8.0-alpine3.12

WORKDIR .

COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

ENV UDACONNECT_API_SERVICE_HOST  host.docker.internal:30001

CMD ["pwd"]
COPY . ./

EXPOSE 3000

CMD ["npm", "start"]

