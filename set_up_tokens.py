import tweepy

consumer_key = "RqJc1h8GxxpXEQwPKiCoJw"
consumer_secret = "6sP8buVdZMuBRXU3z7wsDaeL2ohM7DDIPozun3GIwc"

access_token = "372332469-R6EnkIWd1GWXRnNFakk4LsrlpfsthCddL6gz4lbs"
access_secret = "0hFQj66GbUkF0FxiWTkO4Zx7CrgmjYJwcNsqSqO3w"

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)

print auth.get_authorization_url()

verifier = raw_input('Verifier:')

auth.set_request_token(auth.request_token.key, auth.request_token.secret)

auth.get_access_token(verifier)

print auth.access_token.key
print auth.access_token.secret
