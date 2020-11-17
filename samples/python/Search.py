"""
* 已失效
* Search.py
* this class is for communicating with wechat
* copyright USTC
* 01.11.2020
"""

import glob
import time

import itchat
from itchat.content import TEXT, PICTURE


imgs = []

"""
功能：在图片库中模糊搜索图片
@:param text 需要搜索的图片关键字
"""
def searchImage(text):
    print('收到关键词: ', text)
    for name in glob.glob(r'E:\workspace\python\tran\*'+text+'*.jpg'):
        imgs.append(name)


"""
功能：通过微信发送匹配后的图片
@:param msg 接收的消息
"""
@itchat.msg_register([PICTURE, TEXT])
def text_reply(msg):
    searchImage(msg.text)
    for img in imgs[:6]:
        msg.user.send_image(img)
        time.sleep(0.3)
        print('开始发送表情： ', img)
    imgs.clear()


itchat.auto_login(hotReload=True)
itchat.run()