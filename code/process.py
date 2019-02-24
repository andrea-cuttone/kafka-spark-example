from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import re
import pyspark_cassandra
from pyspark_cassandra import streaming
import time


def sanitize(line):
    line = line.replace('\\n', ' ')
    line = re.sub(r'\\u.{4}', '', line)
    return line


if __name__ == "__main__":
    sc = SparkContext(appName="TwitterGenerator")
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, 10)
    kvs = KafkaUtils.createDirectStream(ssc, ["tweets.topic"], {"metadata.broker.list": "broker:9092"}) 
    
    lines = kvs.map(lambda x: x[1])
    counts = lines\
            .flatMap(lambda line: sanitize(line).split(" "))\
            .filter(lambda w: w.startswith('#'))\
            .map(lambda word: (word, 1))\
            .reduceByKey(lambda a, b: a+b)\
            .map(lambda t: (time.time() * 1000, t[0], t[1]))

    counts.pprint()
    
    counts.saveToCassandra("myks", "test", columns=['timestamp', 'word', 'count']) 

    ssc.start()
    ssc.awaitTermination()
