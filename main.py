#!/usr/bin/env python
#-*-coding:utf-8-*-

import requests
import pymongo
import json
import math
import urllib.parse

class QingtingFM(object):
    def __init__(self,username,password):
        self.username = urllib.parse.quote_plus(username)
        self.password = urllib.parse.quote_plus(password)

    def category_type(self):
        r = requests.get('http://rapi.qingting.fm/categories?type=channel')
        content = json.loads(r.text)
        return content['Data']

    def insert_db(self,title,description,address,category):
        connection = pymongo.MongoClient('mongodb://{0}:{1}@127.0.0.1/qingtingfm?authMechanism=SCRAM-SHA-1'.format(self.username,self.password),27017)
        db = connection.qingtingfm
        post = db.radios
        post.insert({'title':title,'descript':description,'address':address,'category':category})

    def parse_data(self,datas,category):
        for data in datas:
            try:
                title = data['title']
                description = data['description']
                address = 'http://lhttp.qingting.fm/live/'+str(data['content_id'])+'/64k.mp3'
                category = category
            except Exception as e:
                title = data['title']
                address = 'http://lhttp.qingting.fm/live/'+str(data['content_id'])+'/64k.mp3'
                category = category
                description = 'null'
            finally:
                self.insert_db(title,description,address,category)

    def start(self):
        datas = self.category_type()
        count = 0
        for data in datas:
            r = requests.get(" http://rapi.qingting.fm/categories/"+str(data["id"])+"/channels?with_total=true")
            total = json.loads(r.text)['Data']
            total = total['total']
            count+=total
            
            for num in range(1,math.ceil(total/12)+1):
                r2 = requests.get('http://rapi.qingting.fm/categories/'+str(data["id"])+'/channels?with_total=true&page='+str(num)+'&pagesize=50')
                items2 = json.loads(r2.text)['Data']['items']
                self.parse_data(items2,data['title'])

        print('一共爬取：',count)

    
if __name__ == '__main__':
    qtfm = QingtingFM('qtfm','qwe123')
    qtfm.start()
    print('done')