# Big-Data-Analytics

# Real-Time streaming data arriving from twitter streams

### Data Pipeline Flow

![FLOW.PNG](https://github.com/taniyariar/Big-Data-Analytics/blob/master/RealTime%20Twitter%20Streaming%20Pipeline/flow.png)

**1. Scrapper**

1. Collect tweets in real-time with particular hashtag. For example, we will collect all tweets with #guncontrolnow.

2. Filter them by removing emoji symbols and special characters and discard any noisy tweet that do not belong to #guncontrolnow. 
Note that the returned tweet contains both the meta data (e.g., location) and text contents. You will have to keep at least the text
content and the location meta data.

3. After fltering, you need to convert the location meta data of each tweet back to its geolocation info by calling google geo API and send the text and
geolocation info to spark streaming.

4. Scrapper program runs infinitely and takes hash tags as input parameters while running.
      
      
**2. Sentiment Analyzer -**  Sentiment analysis using sentiment analysis tools like NLTK.

**3. Visualization -** Kibana and ElasticSearch

### Data Table Visualization in Kibana

![Data Table in Kibana](https://github.com/taniyariar/Big-Data-Analytics/blob/master/RealTime%20Twitter%20Streaming%20Pipeline/data_table.PNG)

### Heat maps to show the geolocation distribution of tweets

![dashboard.png](https://github.com/taniyariar/Big-Data-Analytics/blob/master/RealTime%20Twitter%20Streaming%20Pipeline/dashboard.PNG)
