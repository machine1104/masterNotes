FROM openjdk:8-alpine
RUN apk --no-cache add curl
COPY ./SOAP-WebService-1.0.jar /usr/app/
WORKDIR /usr/app
EXPOSE 7777
ENTRYPOINT ["java", "-cp", "SOAP-WebService-1.0.jar", "it.sapienza.soapwebservice.Server"]