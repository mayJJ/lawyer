# coding=utf-8
# encoding=utf-8
from pymongo import MongoClient


class DataPersistence(object):
    conn = MongoClient('localhost', 27017)
    db = conn.law
    collection = db.law1

    def save(self, dic):
        try:
            self.collection.save(dic)
            print ('数据插入成功')
        except Exception as e:
            print (e)

    def search(self):
        try:
            result = self.collection.find()
            print (result)
        except Exception as e:
            print(e)