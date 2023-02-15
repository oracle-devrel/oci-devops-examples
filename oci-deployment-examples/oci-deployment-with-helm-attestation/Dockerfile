FROM node:12-alpine

# following https://nodejs.org/en/docs/guides/nodejs-docker-webapp/

WORKDIR /usr/src/node-getting-started

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

# If you are building your code for production
RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 3000
CMD [ "node", "./bin/www" ]