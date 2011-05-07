#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, sys, re

""" 操作対象を持っているアカウント名を指定
アプリ（「ほむにゃん♪」）とアカウントがひもづいているので、
そのセットで切り替える。
"""

account = 'sechiro'         # 投稿先アカウント
conf_file = 'homnyan.conf'  # confはアップしていません。

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

    argvs = sys.argv
    argc = len(argvs)

    if argc > 1 :
        script_name = argvs.pop(0) #shift
        post_message = ' '.join(argvs)
        post_message = unicode(post_message, 'shift-jis') # コマンドプロンプトから引数
        api.update_status(post_message)
        print u'「' + post_message + u'」POST完了にゃ♪'
    else:
        post_message = u"ほむにゃん♪"
        api.update_status(post_message)
        print u'「' + post_message + u'」POST完了にゃ♪'        


if __name__=="__main__":
    main()

