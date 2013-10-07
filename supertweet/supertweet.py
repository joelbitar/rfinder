import datetime
import sys
from twitter import twitter

def post_update(user_name, password, message):
    try:
        twitterApi = twitter.Api(user_name, password)
        twitterApi.PostUpdate(message)
    except:
        pass