from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import json
import textblob
import sys
import datetime
from elasticsearch import Elasticsearch

TCP_IP = 'localhost'
TCP_PORT = 9001

# Pyspark
# create spark configuration
conf = SparkConf()
conf.setAppName('TwitterApp')
conf.setMaster('local[2]')
# create spark context with the above configuration
sc = SparkContext(conf=conf)
#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# create the Streaming Context from spark context with interval size 2 seconds
ssc = StreamingContext(sc, 4)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9001
dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)

######### your processing here ###################
def send_ES(item):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    for part in item:
        try:
            es.index(index='tweetrepo2', doc_type='tweet', body={
                'text': part['text'],
                'location': [part['location']['lon'],part['location']['lat']],
                'timestamp' : datetime.datetime.strptime(part['timestamp'], "%Y-%m-%d %H:%M:%S"),
                'sentiment': part['sentiment']
            })
        except:
            print ("Error" , sys.exc_info()[0])
            
#The sentiment analysis using Textblob
def get_sentiment(tweet_text):
    analysis= textblob.TextBlob(tweet_text)
    if analysis.sentiment.polarity > 0:
        sentiment = 'positive'
    elif analysis.sentiment.polarity == 0:
        sentiment = 'neutral'
    else:
        sentiment = 'negative'
    return sentiment
        
dataStream.pprint()
tweets = dataStream.flatMap(lambda x: x.split('\n'))
tweets_dict= tweets.map(lambda x: json.loads(x))
tweet_sentiment = tweets_dict.map(lambda x: ({'text':x['text'],'location':x['location'],'timestamp':x['timestamp'],'sentiment':get_sentiment(x['text'])})).filter(lambda x :x['location'] is not None )
tweet_sentiment.foreachRDD(lambda rdd: rdd.foreachPartition(send_ES))

#################################################

ssc.start()
ssc.awaitTermination()
