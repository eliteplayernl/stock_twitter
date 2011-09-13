import classify
import tweepy

def pretty_print (number):
  return str(round(number,2))

def faire_le_tweet(bull_count, bear_count, total_count):
  consumer = {"key" : "RqJc1h8GxxpXEQwPKiCoJw",
              "secret" : "6sP8buVdZMuBRXU3z7wsDaeL2ohM7DDIPozun3GIwc"}

  access_token = {"key" : "372332469-R6EnkIWd1GWXRnNFakk4LsrlpfsthCddL6gz4lbs",
                  "secret" : "0hFQj66GbUkF0FxiWTkO4Zx7CrgmjYJwcNsqSqO3w"}

  auth = tweepy.OAuthHandler(consumer["key"], consumer["secret"])
  auth.set_access_token(access_token["key"],access_token["secret"])

  api = tweepy.API(auth)

  percent_bull = (float(bull_count)/total_count)*100
  percent_bear = (float(bear_count)/total_count)*100
  percent_ind = 100 - percent_bear - percent_bull

  api.update_status("Percent of Tweets Bullish: {0}%, Percent of Tweets Bearish: {1}%, Percent Indeterminable: {2}%".format(pretty_print(percent_bull), pretty_print(percent_bear), pretty_print(percent_ind)))


def read_in_data():
  labels = ['bull', 'bear']
  data = {}

  for label in labels:
    f = open(label+'.txt','r')
    data[label] = f.readlines()
    f.close

  return data

def calculate_counts(data):
  nb = classify.NBClassifier()
  nb.train_with_data(data)

  tweets = open("tweets.txt",'r')

  bull_count = 0
  bear_count = 0
  total_count = 0

  for line in tweets.readlines():
    bull_prob = nb.probability(line,'bull')
    bear_prob = nb.probability(line,'bear')
    if bull_prob > bear_prob:
      bull_count += 1
    if bear_prob > bull_prob:
      bear_count += 1
    total_count += 1

  return bull_count, bear_count, total_count

if __name__ == "__main__":
  data = read_in_data()
  bull_count, bear_count, total_count = calculate_counts(data)
  faire_le_tweet(bull_count, bear_count, total_count)
