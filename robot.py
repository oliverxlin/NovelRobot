#coding=utf-8
import itchat
from itchat.content import *
import requests
import json
import tuling
import MisAutoLogin
robot = tuling.tuling()


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])  # type of message
def text_reply(msg):
    text = robot.con_tuling(msg.text)
    if "查询成绩" in msg.text:
        data = msg.text.split(' ')
        if(len(data) <= 2):
            text = "请按格式输入:查询成绩 账号 密码"
        else:
            misauto = MisAutoLogin.MisAutoLogin(data[1], data[2])
     
            text = misauto.jwc_get_score()
    elif "是谁" in msg.text:
        text = "我不知道啊！"
    msg.user.send('%s: %s' % ("Emma", text))


itchat.auto_login(enableCmdQR=2, hotReload=True)

itchat.run()
