#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, sys, re


""" 指定したアカウントの発言をタブ区切りで出力 """
account = 'sechiro'         # データ取得アカウント
conf_file = 'homnyan.conf'  # confはアップしていません。
number = 3200               # 出力POST数
is_monitor = 0              # 画面出力の有無

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

    f = open("csvoutput.txt", "w")
    print 'Start writing.'
    
    for p in tweepy.Cursor(api.user_timeline,account).items(number):
        text = re.sub(r'\r|\n','', unicode(p.text)) 
        output = str(p.user.id) + '\t' + p.user.screen_name + '\t' + text + '\t' + str(p.created_at)       
        if is_monitor == 1:
            print output
        f.write(output.encode('utf-8') + '\n')
    f.close


if __name__=="__main__":
    main()
