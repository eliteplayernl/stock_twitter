import os
import tweepy

def get_list_company_tweets (company_ticker = "", rpp = 100):
  return tweepy.api.search(company_ticker, rpp = rpp)

def flatten_list (list_to_flatten):
  list_to_return = []

  for sub_list in list_to_flatten:
    for item in sub_list:
      list_to_return.append(item.text)

  return list_to_return

companies = ["$MMM", "$AA", "$AXP", "$T"]

super_tweet_list = [get_list_company_tweets(company) for company in companies]

flattened_tweet_list = flatten_list(super_tweet_list)

output_file = open("tweets.txt",'w')

for tweet in flattened_tweet_list:
  output_file.write(tweet.encode('utf-8'))
  output_file.write("\n")


