# -*- coding: utf-8 -*-
"""
Spyder Editor
A simple test file for using twitter api.

The following script uses a username and a list of focused_usernames to
calculate following relationship of them in Twitter.
The result will be saved in graph form node, edges to draw in visjs library.
"""
import twitter
import pickle, os

def connect():
    with open('token_info.p', 'rb') as f:
        token_info = pickle.load(f)
    api = twitter.Api(consumer_key=token_info['consumer_key'],
                  consumer_secret=token_info['consumer_secret'],
                  access_token_key=token_info['access_token_key'],
                  sleep_on_rate_limit=True, # if you want application to sleep
                                             # when excedes its limit rate
                  access_token_secret=token_info['access_token_secret'])
    return api
def save_graph(graph):
    account_map = dict()
    nodes_set = set()
    for key, value in graph.iteritems():
        nodes_set.add(key)
        account_map[key] = graph[key]['label']
        for follower in value['followers']:
            nodes_set.add(follower.id)
            account_map[follower.id] = follower.screen_name
    graph_filename = '../js/graph.js'
    with open(graph_filename, 'w') as f:
        f.write('var nodes = [')
        for node in nodes_set:
            f.write('{id: %d, label: "%s"}, '%(node, account_map[node]))
        f.write('];\n')
        f.write('var edges = [')
        for key, value in graph.iteritems():
            for follower in value['followers']:
                f.write('{from: %d, to: %d},'%(key, follower.id))
        f.write('];')


def main():
    api = connect();
    # TODO my graph should connect related follwers to eachother
    username = 'e_soroush'
    focused_usernames = [] # accounts relationship betweeb your username
    filename = username + '.p'
    force = True
    if os.path.exists(filename) and force == False:
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
    else:
        graph = {}
        connected_ids = []
        root = api.GetUser(screen_name=username)
        myid = root.id
        connected_ids.append(myid)
        graph[myid] = {'label': username, 'followers': api.GetFollowers(screen_name=username)}
        for u in focused_usernames:
            user = api.GetUser(screen_name=u)
            graph[user.id] = {'label': user.screen_name, 'followers': api.GetFollowers()}
        with open(filename, 'wb') as f: 
            pickle.dump(graph, f)
    print('Your connection graph dict: {}'.format(graph))
    save_graph(graph)
    
    
    
if __name__ == '__main__':
    main()
    
    