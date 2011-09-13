import sys, os
import re, string

from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

class NBClassifier:
  def __init__ (self):
    self.feature_count = {}
    self.category_count = {}
 
  def train_with_data(self, data):
    for category, docs in data.items():
      for doc in docs:
        self.train(doc, category)

  def train(self, item, category):
    features = self.get_features(item)

    for f in features:
      self.increment_feature(f, category)

    self.increment_cat(category)

  def get_features(self,document):
    document = re.sub('[%s]' % re.escape(string.punctuation), '', document)
    document = document.lower()
    all_words = [w for w in word_tokenize(document) if len(w) > 3 and len(w) < 16]
    p = PorterStemmer()
    all_words = [p.stem(w) for w in all_words]
    all_words_freq = FreqDist(all_words)

    return all_words_freq

  def increment_feature (self, feature, category):
    self.feature_count.setdefault(feature,{})
    self.feature_count[feature].setdefault(category, 0)
    self.feature_count[feature][category] += 1

  def increment_cat(self, category):
    self.category_count.setdefault(category, 0)
    self.category_count[category] += 1

  #finished with word frequencies, now get probabilities

  def probability(self, item, category):
    cat_prob = self.get_category_count(category) / sum(self.category_count.values())
    return self.document_probability(item,category)*cat_prob

  def get_category_count(self, category):
    if category in self.category_count:
      return float(self.category_count[category])
    else:
      return 0.0

  def document_probability (self, item, category):
    features = self.get_features(item)
    
    p=1
    for feature in features:
      p *= self.weighted_prob(feature, category)
    
    return p

  def weighted_prob(self, f, category, weight=1.0, ap=0.5):
    basic_prob = self.feature_prob(f, category)

    totals = sum([self.get_feature_count(f, category) for category in self.category_count.keys()])

    w_prob = ((weight*ap) + (totals * basic_prob)) / (weight + totals)
    return w_prob

  def feature_prob(self, f, category): # Pr(A|B)
    if self.get_category_count(category) == 0:
      return 0

    return (self.get_feature_count(f, category) / self.get_category_count(category))

  def get_feature_count(self, feature, category):
    if feature in self.feature_count and category in self.feature_count[feature]:
      return float(self.feature_count[feature][category])
    else:
      return 0.0

  def get_category_count(self, category):
    if category in self.category_count:
      return float(self.category_count[category])
    else:
      return 0.0


if __name__ == '__main__':
  labels = ['bull', 'bear']
  data = {}
  for label in labels:
    f = open(label+'.txt','r')
    data[label] = f.readlines()
    f.close

  nb = NBClassifier() 
  nb.train_with_data(data)
  nb.probability("This stock is going higher because of expanded growth possibilites", 'bull')
  nb.probability("This stock is going higher because of expanded growth possibilites", 'bear')
