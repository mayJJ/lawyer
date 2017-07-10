# encoding=utf-8

import requests
from lxml import html
from threading import Thread
from lawyer.DataPersistence import DataPersistence
from multiprocessing.dummy import Pool as ThreadPool
import random
import time
# gevent


# join a city url collection
city_urls = set()
# put url of each city for law list
lawyer_list_urls = set()
# put detail page url
detail_urls = set()


headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, sdch",
    'accept-language': "zh-CN,zh;q=0.8",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'cookie': "route=f29eb48b083f1d2dfe517e6886d338dd; Hm_lvt_ac3abb01a9ad71f2dc9f7344e138c993=1499416706; "
              "Hm_lpvt_ac3abb01a9ad71f2dc9f7344e138c993=1499417024; b=; a=0120101",
    'host': "www.66law.cn",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }


# 从城市页进入, 获得城市标签href
def get_first_request(url):
    # firsr request city page
    r = requests.get(url=url, headers=headers).text
    # parse the page
    tree = html.fromstring(r)
    city_href = tree.xpath("//tr/td[@align='left']/span/a/@href")
    print(city_href)
    for each in city_href:
        # city add in collection
        city_urls.add(each)
    print('>>>>>>>>>>>>>>>>' + str(city_urls.__len__()))

    # 线程1爬取地区的律师列表
    while city_urls.__len__():
        th1 = Thread(target=get_city_lawyer, args=())
        th1.start()
        ra = random.uniform(5, 13)
        time.sleep(ra)

    # 线程2 用于爬取律师详情信息
    # while detail_urls.__len__():
    #     th2 = Thread(target=get_lawyer_info, args=())
    #     th2.start()
    #     ra = random.uniform(1, 5)
    #     time.sleep(ra)


def get_city_lawyer():
    city_href = city_urls.pop()
    city_url = 'http://www.66law.cn' + city_href + 'lawyer/' + 'page_{}.aspx'.format(1)
    # parse_lawyer_list(city_url)

    # print('律师页>>>>>>>>>' + str(lawyer_href))
    # 拿第二页, 用于判断总页数
    get_second_page(city_href)


def parse_lawyer_list(city_url):
    r = requests.get(url=city_url, headers=headers).text
    ra = random.uniform(2, 5)
    time.sleep(ra)
    tree = html.fromstring(r)
    # 拿律师列表中的href，用于爬取详情页面
    lawyer_href = tree.xpath("//ul[@class='find-list find-list5']/li/div/a[@class='ad-hr']/@href")
    lawyer_name = tree.xpath("//ul[@class='find-list find-list5']/li[@class='clearfix tj-lawyer']/p[1]/a/text()")
    lawyer_phone = tree.xpath("//ul[@class='find-list find-list5']/li[@class='clearfix tj-lawyer']/p[1]/b/text()")
    print(lawyer_href, lawyer_name, lawyer_phone)

    for n, p, h in zip(lawyer_name, lawyer_phone, lawyer_href):
        dic = {
            'lawyer_name': n,
            'lawyer_href': p,
            'lawyer_phone': h,
        }
        dp = DataPersistence()
        dp.save(dic)
    clean_detail_url(lawyer_href)


# 清理一遍律师url.
def clean_detail_url(lawyer_href):
    if isinstance(lawyer_href, list):
        for each in lawyer_href:
            if each.startswith('http:'):
                print(each)
                detail_urls.add(each)
            else:

                detail_urls.add('')

    # 将详情页的url添加进详情页集合
    for each_lawyer_href in lawyer_href:
        lawyer_list_urls.add(each_lawyer_href)


# 只有第二页才能拿到总页数
def get_second_page(city_href):
    url = 'http://www.66law.cn' + city_href + 'lawyer/' + 'page_{}.aspx'.format(2)
    r = requests.get(url=url, headers=headers)
    tree = html.fromstring(r.text)
    # 拿到总页数
    total_page = tree.xpath("//div[@id='lawyeronlinepage']/a[last()-1]/text()")

    # 第二页拿不到想要的数据， 说明只有一页
    if len(total_page) == 0:
        pass
    else:
        # 能拿到总页数, 取出页数,构造url
        page = total_page[0]
        more_lawyer_list(page, city_href)


def more_lawyer_list(page, city_href):
    i = 0
    # 还有更多页面, 构造更多的url
    while i < int(page):
        i += 1
        city_url = 'http://www.66law.cn' + city_href + 'lawyer/' + 'page_{}.aspx'.format(str(i))
        parse_lawyer_list(city_url)


def get_lawyer_info():
    r = requests.get(url=detail_urls.pop(), args=()).text
    tree = html.fromstring(r)
    parse_lawyer_info(tree)


def parse_lawyer_info(tree):
    # 姓名：
    name = tree.xpath("")
    # 电话：
    telephone = tree.xpath("")
    # 邮箱:
    email = tree.xpath("")
    # 地址:
    address = tree.xpath("")
    # 专长:
    speciality = tree.xpath("")
    # 执页政号:
    authentication = tree.xpath("")
    # 执业机构:
    company = tree.xpath("")
    # 从业年限:
    work_year = tree.xpath("")

    dic = {
        'name': name,
        'telephone': telephone,
        'email': email,
        'address': address,
        'speciality': speciality,
        'authentication': authentication,
        'company': company,
        'work_year': work_year
    }

    dp = DataPersistence()
    pool = ThreadPool(processes=10)

    pool.apply_async(dp.save(dic))
    pool.close()
    pool.join()


if __name__ == '__main__':
    url = 'http://www.66law.cn/city/'
    get_first_request(url=url)