# coding=utf-8

#=============================================================
# File name: NovelDB.py
# Created time: 2018年08月23日 星期四 16时23分26秒
# Copyright (C) 2018 Richado
# Mail: 16231324@bjtu.edu.cn
#=============================================================


import pymysql

class NovelDB(object):
    def __init__(self, db, host, user, passwd, id_field
            ="chap_id",default_table = "Chaps", charset = "utf8"):
        self.db_name = db
        self.host = host
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.default_table = default_table
        self.id_field = id_field 

    def connect(self):
        try:
            self.db = pymysql.connect(host=self.host,
                                     user=self.user,
                                     passwd=self.passwd,
                                     db=self.db_name,
                                     charset="utf8")
            self.cursor = self.db.cursor()

        except pymysql.Error as e:
            
            raise e

    """
    将章节数据写入数据库
    """
    def write_chap(self,novel_name,url,path,title,number):
        command = """INSERT INTO {} (novel_name,url,path,title,number)
        VALUES('{}', '{}', '{}', '{}',{})"""

        try:
            self.cursor.execute(command.format(self.default_table,novel_name,
                url, path, title,number))

            self.db.commit()

        except pymysql.Error as e:
            raise e
            self.db.rollback()

    
    
     
    """
    获取数据库中小说列表
    """
    def get_novel_list(self):
        pass


    """
    获取指定小说的章节列表,field制定查询内容
    """
    def get_chap_list(self,novel_name,field = ['*']):

        fields = ",".join(field)
        command = """select {} from Chaps where novel_name = '{}' """.format(fields,novel_name)
        print(command) 
        try:
            self.cursor.execute(command)

            results = self.cursor.fetchall()
            
            if len(field) == 1 and field[0] != "*":
                chap_list = []
                #获取每一行数据
                for row in results:
                    chap_list.append(row[0])
 
                return chap_list
            return results 
        except pymysql.Error as e:
            raise e


    """
    添加新的小说
    """
    def add_novel(self,novel_name,url):
        command = """INSERT INTO {} (novel_name,url)
        VALUES('{}', '{}')"""

        try:
            self.cursor.execute(command.format("novels",novel_name, url))
            self.db.commit()

        except pymysql.Error as e:
            raise e
            self.db.rollback()

    """
    获取小说url
    """
    def get_novels(self,novel_name="none"):
        
        if novel_name == "none":
            command = """select url,novel_name from novels"""
        else:
            command = """select url,novel_name from novels where novel_name =
            '{}' """.format(novel_name)
        
        try:
            self.cursor.execute(command)
            
            results = self.cursor.fetchall()
            if len(results) > 0:
                return results
            else:
                return "null"

        except pymysql.Error as e:
            raise e



if __name__ == '__main__':
    db = NovelDB(db='Novel',
                host='127.0.0.1',
                user='root',
                passwd='199814',
                id_field = 'chap_id',
                default_table='Chaps')

    db.connect()

    # db.write_chap(novel_name="测试",url="127.0.0.1",path="~/wechat_robot",title="测试")
    # print(db.get_chap_list("元尊",['number','title','url']))
