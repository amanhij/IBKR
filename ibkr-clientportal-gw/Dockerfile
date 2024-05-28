FROM openjdk:8-jre
WORKDIR /app
COPY . .
EXPOSE 5000
RUN chmod +x ./bin/run.sh
ENTRYPOINT ["./bin/run.sh", "./root/conf.yaml"]
