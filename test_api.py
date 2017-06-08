# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import twitter
import pickle
with open('token_info.p', 'rb') as f:
    token_info = pickle.load(f)
api = twitter.Api(consumer_key=token_info['consumer_key'],
                  consumer_secret=token_info['consumer_secret'],
                  access_token_key=token_info['access_token_key'],
#                  sleep_on_rate_limit=True, # if you want application to sleep
                                             # when excedes its limit rate
                  access_token_secret=token_info['access_token_secret'])

my_followers = api.GetFollowers()
print("My followers are: {}".format(my_followers))

