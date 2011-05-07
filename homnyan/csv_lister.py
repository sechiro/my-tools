#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, sys, re


""" 指定したアカウントの発言をタブ区切りで出力 """
account = 'sechiro'         # データ取得アカウント
conf_file = 'homnyan.conf'  # confはアップしていません。
number = 3200
is_monitor = 0

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
            consumer_key = params[1]
            consumer_secret = params[2]
            access_key = params[3]
            access_secret = params[4]

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

