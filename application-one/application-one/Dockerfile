FROM eclipse-temurin:21-jre-alpine
EXPOSE 8080
COPY target/application-one-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]