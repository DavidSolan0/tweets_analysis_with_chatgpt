import ast
import time
import json
import tweepy
import argparse
import numpy as np
import pandas as pd

from utils import save_pandas_object

from credentials import (
    BEARER_TOKEN,
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)

# Definimos los secret tokens para la escucha y se inicia el cliente
bearer_token = BEARER_TOKEN
api_key = API_KEY
api_secret = API_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

client = tweepy.Client(
    bearer_token,
    api_key,
    api_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

# Se inicializa la API
auth = tweepy.OAuthHandler(
    api_key,
    api_secret,
)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Parámetros de búsqueda
parser = argparse.ArgumentParser()
parser.add_argument("--search_query", help="Twitter search query", nargs="+")
parser.add_argument(
    "--tweets_number", help="Number of desired tweets per search", type=int, default=10
)
parser.add_argument(
    "--parts", help="Number of desired search (iterations) to do", type=int, default=3
)
parser.add_argument(
    "--name",
    help="Name you want to assign to your search",
    type=str,
    default="programming",
)
parser.add_argument("--target_lang", help="Tweets Lang", type=str, default="es")

# Leer parámetros
args = parser.parse_args()

search_terms = args.search_query
parts = args.parts
number_of_tweets = args.tweets_number
desired_language = args.target_lang
folder_name = args.name


# Streaming Class
class MyStream(tweepy.StreamingClient):
    def __init__(
        self,
        bearer_token,
        desired_language="es",
        parts=1,
        number_of_tweets=0,
        folder_name="",
    ):
        super().__init__(bearer_token)
        self.desired_language = desired_language
        self.parts = 1
        self.number_of_tweets = 0
        self.tweets = []
        self.folder_name = folder_name

    def on_connect(self):
        print("Connected")

    def on_tweet(self, tweet):
        retweeted_status = tweet.get("retweeted_status")
        if not retweeted_status and tweet.get("lang") == self.desired_language:
            time.sleep(0.2)
            self.process_tweet(tweet)

    def process_tweet(self, tweet):
        extended_tweet = tweet.get("extended_tweet")
        if extended_tweet:
            text = extended_tweet.get("full_text")
        else:
            text = tweet.get("text")

        referenced_tweets = tweet.get("referenced_tweets")
        author_id = tweet.get("author_id")
        created_at = tweet.get("created_at")

        tweet_data = {
            "created_at": created_at,
            "text": tweet["text"],
            "public_metrics": tweet.get("public_metrics"),
            "context_annotations": tweet.get("context_annotations"),
            "entities": tweet.get("entities"),
            "referenced_tweets": referenced_tweets,
        }

        self.tweets.append(tweet_data)
        self.number_of_tweets += 1

    def on_data(self, raw_data):
        try:
            tweet = json.loads(raw_data)["data"]
            self.on_tweet(tweet)
            time.sleep(0.2)
            if self.number_of_tweets == number_of_tweets:
                print(f"Entered writing part {self.parts}")
                name = f"data_{self.parts}.csv"
                df = pd.DataFrame(self.tweets)
                save_pandas_object(df, "..\data", self.folder_name, name)
                self.number_of_tweets = 0
                self.tweets = []
                self.parts += 1
            if self.parts == parts:
                self.disconnect()
        except Exception as e:
            print(e)

    def on_disconnect(self):
        print("Disconnected")


stream = MyStream(
    bearer_token=bearer_token,
    desired_language=desired_language,
    parts=parts,
    number_of_tweets=number_of_tweets,
    folder_name=folder_name,
)

# Eliminar reglas anteriores
result_count = stream.get_rules().meta["result_count"]
print(f"Hay {result_count} queries previos")
if result_count > 0:
    for i in range(result_count):
        prev_id = stream.get_rules().data[0].id
        stream.delete_rules(prev_id)

# Añadir nuevas reglas
for term in search_terms:
    print(f"Se añade el query '{term}'")
    stream.add_rules(tweepy.StreamRule(term))

# Streaming
stream.filter(
    tweet_fields=[
        "referenced_tweets",
        "entities",
        "created_at",
        "public_metrics",
        "context_annotations",
        "lang",
    ]
)
