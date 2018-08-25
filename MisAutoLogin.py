#coding:utf-8
import requests
import re
import sys
from time import sleep
import urllib
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from django.views.decorators.csrf import csrf_protect

class MisAutoLogin(object):
    def __init__(self,number,pwd):
        # set of url
        self.mislogin_url = 'https://mis.bjtu.edu.cn'
        self.mis_url = 'https://mis.bjtu.edu.cn/home/'
        self.jwc_url = self.mislogin_url + '/module/module/322/'
        self.submit_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit'
        self.kua_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=cross&page=29'
        self.zyxx_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/'
        self.rx_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?'
        self.jwc_score_url = 'https://dean.bjtu.edu.cn/score/scores/stu/view/'
       
        self.header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',   
        }
        self.login_data = {
            'loginname': number,
            'password': pwd,
        }      
        self.session = requests.session()
       

    def mis_auto_login(self):
        req = self.session.get(self.mislogin_url)

        login_url = req.url
        self.header['Referer'] = req.url
        
        soup = BeautifulSoup(req.content, 'lxml')
        csrfmiddlewaretoken = soup.find(
            attrs={'name': 'csrfmiddlewaretoken'}).attrs['value']

        self.login_data['csrfmiddlewaretoken'] = csrfmiddlewaretoken
        
        next = str(req.url).replace('%3F', urllib.parse.unquote('%3F'), 10).replace('%3D', urllib.parse.unquote(
            '%3D'), 10).replace('%26', urllib.parse.unquote('%26'), 10).replace('%3A', urllib.parse.unquote('%3A'), 10)
        next = next[next.index("next=") + len('next='):]
        self.login_data['next'] = next

        # 模拟登陆mis
        req = self.session.post(
            login_url, data=self.login_data, headers=self.header)


    def jwc_login(self):
        #先登陆mis
        self.mis_auto_login()

        # 进入jwc界面
        resp = self.session.get(self.jwc_url)
        html = resp.content.decode('utf-8','ignore')

        #从中转界面获取url跳转
        soup = BeautifulSoup(html, 'lxml')
        self.header['Referer'] = self.jwc_url

        resp = self.session.get(soup.form['action'], headers= self.header)
        html = resp.content.decode('utf-8','ignore')

        if self.check_login_dean(html):
            return True
        return False

    def check_login_dean(self, html_content):
        soup = BeautifulSoup(html_content, 'lxml')

        if soup.find('span').attrs['class'][0] == 'user-info':
            print("成功登陆教务系统")
            return True
        else:
            print("登陆教务系统失败")
            return False

    def jwc_get_score(self):
        self.jwc_login()
        resp = self.session.get(self.jwc_score_url, headers= self.header)
        html = resp.content.decode('utf-8','ignore')
        print(html)
        soup = BeautifulSoup(html,'lxml')
        p = soup.find_all('tr')
        count1 = 0
        count2 = 0
        ans = ""
        for index in range(len(p)):
            if index == 0:
                continue
            tds = p[index].find_all('td')
            lesson = tds[2].text.replace(' ','').replace('\n','')[7:]
            score = tds[4].text.replace(' ','').replace('\n','')
            if score != "***":
                count2 += 1
            print("课程：{} \n成绩：{}\n\n".format(lesson,score))
            ans = ans + "课程：{} \n成绩：{}\n\n".format(lesson,score)
            count1 += 1
        print("总课程数：{},已出成绩：{}\n".format(count1,count2))
        return ans
    
if __name__ == '__main__':
    qk = MisAutoLogin("16231324","183812")
    qk.jwc_get_score()
