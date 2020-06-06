FROM openjdk:8-alpine
RUN apk --no-cache add curl
COPY ./JMSServant-1.0-SNAPSHOT-jar-with-dependencies.jar /usr/app/
WORKDIR /usr/app
ENTRYPOINT ["java", "-cp", "JMSServant-1.0-SNAPSHOT-jar-with-dependencies.jar", "server.StockMarketServer"]