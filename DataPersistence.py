# encoding=utf-8
from pymongo import MongoClient


class DataPersistence(object):
    conn = MongoClient('localhost', 27017)
    db = conn.law
    collection = db.law2

    collection2 = db.city_url

    def save_mongo_lawyers(self, dic):
        try:
            self.collection.save(dic)
            print('数据插入成功')
        except Exception as e:
            print(e)

    def search(self, dic):
        try:
            lh = self.collection.find({
                'lawyer_href': dic['lawyer_href']
            }).count()

            # 只有表中不存在时才会插入该条数据
            if lh != 0:
                pass
            else:
                self.save_mongo_lawyers(dic)
        except Exception as e:
            print(e)

    def save_city_url(self, city_url):
        try:
            self.collection2.save({'city_url': city_url})
        except Exception as e:
            print(e)

    def write_file(self):
        results = self.collection.find()

        with open('lawyer_info.txt', 'a+', encoding='utf-8') as f:
            f.write('律师姓名')
            f.write('电话')
            f.write('个人网址')
            f.write('爬取时间')
            for result in results:
                print(result)
                f.write(str(result['lawyer_name']) + '      ')
                f.write(str(result['lawyer_phone']) + '       ')
                f.write(str(result['lawyer_href']) + '\n')
        f.close()

if __name__ == '__main__':
    dp = DataPersistence()
    dp.write_file()