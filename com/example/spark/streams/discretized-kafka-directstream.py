from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        sys.exit(-1)

    sc = SparkContext(appName="discretize-kafka-stream")
    ssc = StreamingContext(sc, 1)

    zkQuorum="quickstart-bigdata:2181"
    topic = "structured-stream-topic"

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": "quickstart-bigdata:9092"})
    lines = kvs.map(lambda x: x[1])

    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()

