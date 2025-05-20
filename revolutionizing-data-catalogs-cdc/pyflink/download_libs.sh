#!/bin/bash

mkdir -p ./lib


curl -o ./lib/flink-sql-connector-postgres-cdc-3.0.1.jar https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-postgres-cdc/3.0.1/flink-sql-connector-postgres-cdc-3.0.1.jar
curl -o ./lib/flink-sql-connector-kafka-3.4.0-1.20.jar https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.4.0-1.20/flink-sql-connector-kafka-3.4.0-1.20.jar
curl -o ./lib/flink-sql-connector-elasticsearch7-3.0.1-1.17.jar https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-elasticsearch7/3.0.1-1.17/flink-sql-connector-elasticsearch7-3.0.1-1.17.jar
echo "Libs downloaded successfully"
