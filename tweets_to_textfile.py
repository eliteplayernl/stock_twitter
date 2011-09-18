import os
import tweepy
import random

def get_list_company_tweets (company_ticker = "", rpp = 100):
  return tweepy.api.search(company_ticker, rpp = rpp)

def flatten_list (list_to_flatten):
  list_to_return = []

  for sub_list in list_to_flatten:
    for item in sub_list:
      list_to_return.append(item.text)

  return list_to_return

companies = []

tickers = open("ticker.txt", 'r')

for ticker in tickers.readlines():
  companies.append(ticker.rstrip('\n'))

random.shuffle(companies)
companies = companies[:150]
companies = ["$" + comp for comp in companies]

super_tweet_list = []

for company in companies:
  try: 
    super_tweet_list.append(get_list_company_tweets(company))
  except:
    pass

flattened_tweet_list = flatten_list(super_tweet_list)

output_file = open("tweets.txt",'w')

for tweet in flattened_tweet_list:
  output_file.write(tweet.encode('utf-8'))
  output_file.write("\n")

output_file.close()
