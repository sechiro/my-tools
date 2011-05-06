#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

# JSON
try:
    import simplejson as json
except ImportError:
    import json


def main():
    """ Class Usage Sample"""

    """ qpstudy参加者一覧出力（中身はiaraさんが立てたATNDイベントのユーザ取得） """
    #get_qp()

    """ キーワード検索の場合は、文字列を直接、もしくはリストで渡す """
    get_users_by_keyword(keyword='メイド', keyword_or=['擬人化','サーバ']) # keywordはURLにこのまま代入するので、Unicodeにしない。


def get_qp():
    """ Sample of get_users_in_events """
    atnd = atnd_api()
    atnd.count = 100 # 取得イベント上限数
    atnd.owner_id = 7710 # qpstudyのリーダー、iaraさんのATND ID
    events = atnd.get_users_in_events()
    print u'================================\n' \
        + u'以下のイベントの参加者を取得します。\n' \
        + u'================================'
    for event in events:
        print str(event['event_id']) + ' ' + event['title']

    total_users = []    # 累計参加者
    temp_total = []    # 累計参加者差分を取るための一時データ

    """ 各イベントの参加者一覧を出力し、累計参加者一覧を更新 """
    """ 出力形式: ATND上の名前、Twitter ID、参加有無（1 or 0）"""
    for event in events:
        print u'\n================================'        
        print str(event['event_id']) + ' ' + event['title']
        print u'================================'                
        users_info = event['users']
        temp_total = total_users
        for user_info in users_info:
            print user_info['nickname'] + ' ' + str(user_info['twitter_id']) + ' ' + str(user_info['status'])
            
            flag = 0
            for total_user in temp_total:
                if user_info['user_id'] == total_user['user_id']:
                    flag = 1
                    break
                    
            if flag == 0:
                total_users.append( user_info ) # 各回の参加有無のstatusは使わないので取り込まない。

    """ 累計参加者出力 """                
    print u'================================\n' \
        + u'これまでの累計参加者' + str(len(total_users)) + '\n' \
        + u'================================'

    print u'=====================\n' \
        + u'User with Twitter ID\n' \
        + u'====================='

    """ Twitter ID 一覧のみファイルに出力 """
    f = open('total_twusers.txt', 'w')
    for user_info in total_users:
        if user_info['twitter_id'] != None:
            print user_info['nickname'] + ' ' + str(user_info['twitter_id'])
            f.write(user_info['twitter_id'] + '\n')
            
    print u'=====================\n' \
        + u'User w/o Twitter ID\n' \
        + u'====================='
    for user_info in total_users:
        if user_info['twitter_id'] == None:
            print user_info['nickname'] + ' ' + str(user_info['twitter_id'])


def get_users_by_keyword(keyword='', keyword_or=''):
    """ Sample of get_users_by_event_id """
    atnd = atnd_api()
    atnd.count = 100 # 取得イベント上限数
    atnd.keyword = keyword # strのlistもしくは単体のstr
    events = atnd.get_events()
    print u'================================\n' \
        + u'以下のイベントの参加者を取得します。\n' \
        + u'================================'
    for event_id in events.keys():
        print str(event_id) + ' ' + events[event_id]

    total_users = []    # 累計参加者
    temp_total = []     # 累計参加者差分を取るための一時データ

    """ 各イベントの参加者一覧を出力し、累計参加者一覧を更新 """
    """ 出力形式: ATND上の名前、Twitter ID、参加有無（1 or 0）"""
    for event_id in events.keys():
        print u'\n================================'        
        print str(event_id) + ' ' + events[event_id]
        print u'================================'                
        users_info = atnd.get_users_by_event_id(event_id)

        temp_total = total_users
        for user_info in users_info:
            print user_info['nickname'] + ' ' + str(user_info['twitter_id']) + ' ' + str(user_info['status'])
            flag = 0
            for total_user in temp_total:
                if user_info['user_id'] == str(total_user['user_id']):
                    flag = 1
                    break
                    
            if flag == 0:
                total_users.append( user_info ) # 各回の参加有無のstatusは使わないので取り込まない。

    """ 累計参加者出力 """                
    print u'================================\n' \
        + u'これまでの累計参加者' + str(len(total_users)) + '\n' \
        + u'================================'

    print u'=====================\n' \
        + u'User with Twitter ID\n' \
        + u'====================='

    """ Twitter ID 一覧のみファイルに出力 """
    f = open('total_twusers.txt', 'w')
    for user_info in total_users:
        if user_info['twitter_id'] != None:
            print user_info['nickname'] + ' ' + str(user_info['twitter_id'])
            f.write(user_info['twitter_id'] + '\n')
            
    print u'=====================\n' \
        + u'User w/o Twitter ID\n' \
        + u'====================='
    for user_info in total_users:
        if user_info['twitter_id'] == None:
            print user_info['nickname'] + ' ' + str(user_info['twitter_id'])
            
        
""" 以下、Class定義 """
class atnd_api_base:
    def __init__(self):
        self.event_id = self.user_id = self.nickname = self.twiter_id = \
                        self.owner_id = self.owner_nickname = self.owner_twitter_id = ''
        self.start = '1'
        self.count = '10'
        self.format = 'json'
        
class atnd_api(atnd_api_base):        
    def __init__(self):
        atnd_api_base.__init__(self)
        self.keyword = self.keyword_or = self.ym = self.ymd = ymd = ''

    """ Return ATND Events in dict format"""
    def get_events(self):
        url = 'http://api.atnd.org/events/?' + \
                        'user_id=' + str(self.user_id) + \
                        '&event_id=' + str(self.event_id) + \
                        '&user_id=' + str(self.user_id) + \
                        '&nickname=' + str(self.nickname) + \
                        '&twitter_id=' + str(self.twiter_id) + \
                        '&owner_id=' + str(self.owner_id) + \
                        '&owner_nickname=' + str(self.owner_nickname) + \
                        '&owner_twitter_id=' + str(self.owner_twitter_id) + \
                        '&start=' + str(self.start) + \
                        '&count=' + str(self.count) + \
                        '&format=' + str(self.format) + \
                        '&ym=' + str(self.ym) + \
                        '&ymd=' + str(self.ymd)

        keyword = self.keyword
        if isinstance(keyword, list):
            for word in keyword:
                url += '&keyword=' + str(word)
                
        else:
            url += '&keyword=' + str(keyword)

        keyword_or = self.keyword_or
        if isinstance(keyword_or, list):
            for word in keyword_or:
                url += '&keyword_or=' + str(word)                
        else:
            url += '&keyword_or=' + str(keyword_or)            
        

        # デバッグ用Request URL出力
        #print u'=====================\n' \
        #    + u'ATND API Request URL\n' \
        #    + u'=====================' 
        #print url + '\n'
        
        p = urllib.urlopen(url)
        data = json.loads(p.read())
        events = data['events']
        result = {}
        for event in events:
            result[event['event_id']] = event['title']
        return result

    def get_users_in_events(self):
        url = 'http://api.atnd.org/events/users/?' + \
                        'user_id=' + str(self.user_id) + \
                        '&event_id=' + str(self.event_id) + \
                        '&user_id=' + str(self.user_id) + \
                        '&nickname=' + str(self.nickname) + \
                        '&twitter_id=' + str(self.twiter_id) + \
                        '&owner_id=' + str(self.owner_id) + \
                        '&owner_nickname=' + str(self.owner_nickname) + \
                        '&owner_twitter_id=' + str(self.owner_twitter_id) + \
                        '&start=' + str(self.start) + \
                        '&count=' + str(self.count) + \
                        '&format=' + str(self.format)

        # デバッグ用Request URL出力
        #print u'=====================\n' \
        #    + u'ATND API Request URL\n' \
        #    + u'=====================' 
        #print url + '\n'        

        p = urllib.urlopen(url)
        data = json.loads(p.read())
        events = data['events']                
        return events  

    def get_users_by_event_id(self, event_id):
        url = 'http://api.atnd.org/events/users/?' + \
                        'event_id=' + str(event_id) + \
                        '&start=' + str(self.start) + \
                        '&count=' + str(self.count) + \
                        '&format=' + str(self.format)
        
        p = urllib.urlopen(url)
        data = json.loads(p.read())
        events = data['events']
        users_info = events[0]['users']       
        return users_info
              

if __name__=="__main__":
    main()
