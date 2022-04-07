FROM ghcr.io/graalvm/graalvm-ce:latest

WORKDIR /sample-polyglot-app

COPY package.json .

RUN  gu install nodejs
RUN  gu install R

COPY . .

CMD ["node", "--jvm", "--polyglot", "server.js"]
       


