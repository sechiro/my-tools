#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

# JSON
try:
    import simplejson as json
except ImportError:
    import json

ATND_EVENT_URL='http://api.atnd.org/events/?format=json&count=%s&owner_id=%s'
ATND_USERS_URL='http://api.atnd.org/events/users/?format=json&count=%s&event_id=%s'
iara = 7710 # リーダーのATND ID
count = 100  # 検索上限イベント数(Max:100)

def main():
    qpstudies = get_qpid()
    print u'================================\n' \
        + u'以下のイベントの参加者を取得します。\n' \
        + u'================================'
    for k in qpstudies.keys():
        print str(k) + ' ' + qpstudies[k]

    total_users = []
    temp_total = []
    for k in qpstudies.keys():
        print u'================================'        
        print str(k) + ' ' + qpstudies[k]
        print u'================================'                
        users_info = get_users(k) # nickname:twitter_id:status

        temp_total = total_users
        for user_info in users_info:
            flag = 0
            for total_user in temp_total:
                if user_info[0] == total_user[0] and total_user[0] != '':
                    flag = 1
                    break
                    
            if flag == 0:
                total_users.append( (user_info[0],user_info[1]) ) # delete status
                    
    print u'================================\n' \
        + u'これまでの累計参加者 (total: ' + str( len(total_users) ) + '\n' \
        + u'================================'

    print u'=====================\n' \
        + u'User with Twitter ID\n' \
        + u'====================='
    f = open('qptwuser.txt', 'w')
    for total_user in total_users:
        if total_user[1] != None:
            print '%s\t%s' % total_user
            f.write(total_user[1] + '\n')
            
    print u'=====================\n' \
        + u'User w/o Twitter ID\n' \
        + u'====================='
    for total_user in total_users:
        if total_user[1] == None:
            print '%s\t%s' % total_user
        

def get_qpid():
    url = ATND_EVENT_URL % ( count, iara )
    p = urllib.urlopen(url)
    data = json.loads(p.read())
    events = data['events']
    result = {}
    for event in events:
        result[event['event_id']] = event['title']
        #print event['title'] + ' ' + str(event['event_id'])
    return result

def get_users(event_id):
    url = ATND_USERS_URL % ( count, event_id )
    p = urllib.urlopen(url)
    data = json.loads(p.read())
    events = data['events']
    users = events[0]['users']
    users_info = []
    for user in users:
        user_info = (user['nickname'], user['twitter_id'], user['status']) 
        print '%s:%s:%s' % user_info
        users_info.append(user_info)        
    return users_info

if __name__=="__main__":
    main()
