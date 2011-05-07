#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, sys, re, os

""" 操作対象を持っているアカウント名を指定
アプリ（「ほむにゃん♪」）とアカウントがひもづいているので、
そのセットで切り替える。
"""

account = 'sechiro'         # リストを持っているアカウント
list_file = 'list.txt'      # Twitter ID一覧（各行にアカウント名）
list_name = u'ほむほむ'      # 追加対象のリスト名
conf_file = 'homnyan.conf'  # confはアップしていません。

# ほむにゃん♪のアプリ側キー
consumer_key = "ZqI1Dufey1tRzQDqHnZwew"
consumer_secret = "ljD03gFAEhpjrFciD4RKJMjE4mpVgQjjwxg2puS1ak"

def main():
    f = open(conf_file, "r")
    confs = []
    line = f.readline()
    while line:
        if re.match("#", line):
            line = f.readline()            
            continue
        
        conf = line.rstrip()
        confs.append(conf)
        line = f.readline()
    f.close

    for conf in confs:
        params = conf.split(',')
        if params[0] == account:    
            access_key = params[1]
            access_secret = params[2]
            
    
    # create OAuth handler                                                      
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)                   
    # set access token to OAuth handler                                         
    auth.set_access_token(access_key, access_secret)                            
    # create API                                                                
    api = tweepy.API(auth_handler=auth) 
    members = []
    
    f = open(list_file, "r")
    line = f.readline()
    while line:
        if re.match("#", line):
            line = f.readline()            
            continue

        member = line.rstrip()
        #print member
        members.append(member)
        line = f.readline()
    f.close        
    print members

    for member in members:
        try:
            listid = api.get_list(account, list_name).id
            print listid
            result = api.add_list_member(listid, member)
            print member + u'を「' + result.slug + u'（' + str(listid) + u'）」リストに追加しました。'
            
        except:
            print "exc_info: %s" % str(sys.exc_info())


def get_list_members(api, id, listname):
    """ get list_members """
    mem_dict = {}
    m_count = api.get_list(id, listname).member_count
    for p in tweepy.Cursor(api.list_members, id, listname).items(m_count):
        try:
            mem_dict[p.screen_name] = re.sub(r'\r|\n','', p.description)
        except:
            mem_dict[p.screen_name] = '(No description.)'

    for k in mem_dict.keys():
        print k + '\t' +mem_dict[k]
        

if __name__ == '__main__':
    main()
