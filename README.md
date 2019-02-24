An example data pipeline to count Twitter hashtags, built with Docker-Compose, Kafka, PySpark and Cassandra.

# Prerequisites
- Install Docker and Docker-Compose
- Fill in config.py with your access tokens from [Twitter Developer API](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)

# Setup
Create the network:

```docker network create kafka-network```

Start Kafka:

```docker-compose -f docker-compose.kafka.yml up -d```

Start the rest of the services and start pushing Tweets:

```docker-compose build && docker-compose up```

Launch Cassandra CQLSH and run cassandra.cql to create the table:

```docker-compose exec cassandra cqlsh```

Start Spark stream processing:

```docker-compose exec sparksubmit bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11/2.0.0,anguenot:pyspark-cassandra:0.10.1,commons-configuration:commons-configuration:1.6 --conf spark.cassandra.connection.host=cassandra code/process.py```

Open again CQLSH:

```docker-compose exec cassandra cqlsh```

Finally the table content:

```SELECT * FROM MYKS.TEST;```
