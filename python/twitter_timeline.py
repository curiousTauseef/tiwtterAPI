#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 23:28:50 2017
This script is for storing tweets from all following accounts
@author: esoroush
"""

#!/usr/bin/env python
# encoding: utf-8

import csv, os
from twitter_connection import connect


def get_all_tweets(screen_name):
    if os.path.exists('%s_tweets.csv' % screen_name):
        return
    else:
        print screen_name
	api = connect()
	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.GetUserTimeline(screen_name=screen_name)
    if len(new_tweets) == 0:
        return
    else:
        print new_tweets[0].text
	#save most recent tweets
	alltweets.extend(new_tweets)
    

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.GetUserTimeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print("...%s tweets downloaded so far" % (len(alltweets)))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode('utf8')] for tweet in alltweets]

    
	#write the csv
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)


def get_following(screen_name):
    api = connect()
    return api.GetFriends(screen_name=screen_name)

def get_all_following_tweets(screen_name):
    following = get_following(screen_name)
    i = 0
    for f in following:
        i+=1
        get_all_tweets(f.screen_name)
        print i
    
    
    
if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_following_tweets("e_soroush")
