import tweepy  # Tweepy library to interact with Twitter's API
import time    # Time library for controlling rate limits

# Authentication credentials required to access Twitter API
consumer_key = ''  # Consumer API key
consumer_secret = ''  # Consumer API secret key
access_token = ''  # Access token
access_token_secret = ''  # Access token secret

# Setting up OAuth1 authentication handler with credentials
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

# Use the authentication object to authenticate with the Twitter API
api = tweepy.API(auth)

# Grabs recent public tweets from the home timeline and prints their text
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)  # Prints the text of each tweet

# Example of printing user details (currently commented out)
# This would fetch and display the authenticated user's profile information
# user = api.me()
# print(user.name)  # Prints the name of the authenticated user
# print(user.screen_name)  # Prints the screen name (handle) of the authenticated user
# print(user.followers_count)  # Prints the number of followers

# Function to handle rate limit exceptions and prevent API overload
# This ensures that the bot doesn't exceed the rate limit by pausing when necessary
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()  # Yield the next item in the cursor (pagination)
    except tweepy.RateLimitError:
        # If rate limit is exceeded, wait for 500 seconds (adjust based on Twitter's rate limit guidelines)
        time.sleep(500)

# Narcissistic Bot section
# The bot will search for tweets containing a specific string and like them
search_string = 'narcississtic search string'  # Set the search query string
numberOfTweets = 2  # Set the number of tweets to interact with

# Cursor to search for tweets containing the search string
for tweet in tweepy.Cursor(api.search, search_string).items(numberOfTweets):
    try:
        # Like the tweet (favorite it)
        tweet.favorite()
        print('I like that tweet')  # Confirmation message when a tweet is liked
    except tweepy.TweepError as e:
        # Handle any exceptions (e.g., rate limits, or if the tweet has already been liked)
        print(e.reason)
    except StopIteration:
        # Stop iterating if no more tweets are available
        break

# Generous Bot section
# This bot will follow specific users who follow the authenticated user
# It can be configured to follow all users or only specific users

# Use the limit handler to avoid hitting rate limits while fetching followers
for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    if follower.name == 'followers username':  # Replace with the username of the follower you want to follow
        follower.follow()  # Follow that specific user
        break  # Exit the loop after following the specified user
