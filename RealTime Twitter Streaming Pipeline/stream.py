import json 
import requests
import tweepy
import socket
import re

ACCESS_TOKEN = 'your access token'
ACCESS_SECRET = 'your access secret'
CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

hashtag = '#guncontrolnow'

TCP_IP = 'localhost'
TCP_PORT = 9001
# create sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()    

def filter_tweet(tweet):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    tweet = emoji_pattern.sub(r'', tweet) 
    tweet = tweet.replace("RT", "")
    tweet= ' '.join(re.sub("([^a-zA-Z0-9 .#])|(@\S*[\s, .])|(\w+:\/\/\S+)|http\S+", " ", tweet).split())
    return tweet

    
def get_geolatlong(loc):
    #print(loc)
    if loc is not  None:
        par = {'sensor': 'false', 'address': loc}
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=par)
        output = r.json()['results']
        for out in output:
            loc = {'lat': out['geometry']['location']['lat'],'lon': out['geometry']['location']['lng']}
            return loc

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        ts = status.created_at
        #print("____________tweet_____________")
        #print(status.created_at)
        doc = {'text': filter_tweet(status.text),'location': get_geolatlong(status.user.location),'timestamp' :ts.strftime("%Y-%m-%d %H:%M:%S")}
        #print(doc)
        conn.send((json.dumps(doc) + "\n").encode('utf-8'))
    
    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)

myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
myStream.filter(track=[hashtag])


