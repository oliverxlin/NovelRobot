# coding=utf-8

#=============================================================
# File name: NovelSpider.py
# Created time: 2018年08月23日 星期四 01时34分34秒
# Copyright (C) 2018 Richado
# Mail: 16231324@bjtu.edu.cn
#=============================================================
import requests
import re
import sys
from time import sleep
import urllib
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import random
import NovelDB
import logging
import os
import time
import threading



LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

class NovelSpider(object):
    def __init__(self):

        self.url = "http://www.biqiuge.com"
        self.session = requests.session()
            
        self.db = NovelDB.NovelDB(db='Novel',
                    host='127.0.0.1',
                    user='root',
                    passwd='199814',
                    id_field = 'chap_id',
                    default_table='Chaps')

        self.db.connect()


    
    """
    更新数据库中的章节
    """
    def update_list_sql(self):
       
        #从数据库中读出小说名
        novels = self.db.get_novels()
        
        #更新每一本小说
        for novel in novels:

            novel_name = novel[1]
            
            chap_list = self.get_list_online(novel_name)
            chap_list_sql = self.db.get_chap_list(novel_name,field=["title"])
            
            #对新小说创建文件目录 
            if not os.path.exists(novel_name):
                os.mkdir(novel_name)   

            if len(chap_list) > len(chap_list_sql):
                
                number = 1
                threads = []
                for chap in chap_list:
                    if chap['title'] not in chap_list_sql:
                        
                        threads.append(threading.Thread(target=self.get_content,args=(chap['url'],novel_name,number,chap['title'])))
                        logging.info("章节更新:{}".format(chap['title']))
                        self.db.write_chap(novel_name=novel_name,url=chap['url'],path="~/NovelRobot/"+novel_name,title=chap['title'],number=number)
                    number += 1

                for t in threads:
                    t.start()
                    sleep(0.1)
    
    
    """
    获取在线章节列表
    """
    def get_list_online(self,novel_name):
        req = self.session.get(self.db.get_novels(novel_name)[0][0])#从数据库中获得小说url
        html = req.content.decode('gbk','ignore')
        soup = BeautifulSoup(html,'lxml')
        dds = soup.find_all('dd')
        
        chap_list = []
        
        for chap in dds[6:]:
            #一般重复章节连续出现，用于去重
            if len(chap_list) == 0 or self.url + chap.a['href'] != chap_list[-1]['url']:
                chap_list.append({"title":chap.text, "url":self.url + chap.a['href']})

        return chap_list
    
    
    """
    获取最新的6章节
    """
    def get_newest_online(self,novel_name):
        chap_list = self.db.get_chap_list(novel_name,field=['title'])
        print(chap_list[-1:-7:-1])


    """
    添加新的小说
    """
    def add_new_novel(self,novel_name,novel_url):
        self.db.add_novel(novel_name,novel_url)
        self.update_list_sql()

    """
    获取小说内容
    """

    def get_content(self,url,novel_name,number,title):
        
        path = novel_name + "/{}".format(number)
        logging.info("正在下载第{}章{}".format(number,title))
        req = self.session.get(url)
        
        #获取小说文章
        html = req.text
        soup = BeautifulSoup(html,'lxml')
        content = soup.find('div',id="content")        
        content = content.get_text().replace("\t"," ").split(" ")        
            
        f = open(path,"w")
        f.write("\t"+title+"\n\n")
        for line in content:
            f.write("\t" + line.strip() + "\n\n")
        f.close()



if __name__ == "__main__":
    spider = NovelSpider()
    #spider.add_new_novel("飞剑问道","http://www.biqiuge.com/book/24277/")
    spider.update_list_sql()
    #spider.get_list("元尊")
    #spider.update_list_sql()
    #rep =requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxa0786cda5581e5cd&secret=72aa571a446c26486b68924b5de9f862")
    #print(rep.text)i
    # print(spider.get_list_online("飞剑问道"))
    #spider.get_newest_online("飞剑问道")
