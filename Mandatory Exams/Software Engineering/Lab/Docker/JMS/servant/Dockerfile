FROM openjdk:8-alpine
RUN apk --no-cache add curl
COPY ./JMSServant1.0SNAPSHOTjarwithdependencies.jar /usr/app/
WORKDIR /usr/app
ENTRYPOINT ["java", "-cp", "JMSServant1.0SNAPSHOTjarwithdependencies.jar", "it.sapienza.softeng.jmsservant.StockMarketServer"]