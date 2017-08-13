#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 00:04:02 2017
This script is for connection considerations

@author: esoroush
"""

import twitter
import pickle

def connect():
    with open('token_info.p', 'rb') as f:
        token_info = pickle.load(f)
    api = twitter.Api(consumer_key=token_info['consumer_key'],
                  consumer_secret=token_info['consumer_secret'],
                  access_token_key=token_info['access_token_key'],
                  sleep_on_rate_limit=True, # if you want application to sleep
                                             # when excedes its limit rate
                  input_encoding='utf8',                        
                  access_token_secret=token_info['access_token_secret'])
    return api