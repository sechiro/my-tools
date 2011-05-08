#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, sys, re


""" 指定したアカウントの発言をタブ区切りで出力 """
account = 'sechiro'         # 自分のアカウント
target_user = 'sechirro'    # データ取得対象アカウント
conf_file = 'homnyan.conf'  # confはアップしていません。
number = 3200               # 出力POST数(Max: 3200)
is_monitor = 0              # 画面出力の有無
since_id = 0                # このID以降のPOSTを取得します。
output_file = target_user + '.csv'

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

    f = open(output_file, "w")
    print 'Start writing.'
    
    for p in tweepy.Cursor(api.user_timeline,target_user,since_id).items(number):
        text = re.sub(r'\r|\n','', unicode(p.text))
        #print dir(p)
        output = str(p.user.id) + '\t' + p.user.screen_name + '\t' + text + \
                 '\t' + str(p.created_at) + '\t' + str(p.id) + '\t' + p.source
        if is_monitor == 1:
            print output
        f.write(output.encode('utf-8') + '\n')
    f.close


if __name__=="__main__":
    main()

