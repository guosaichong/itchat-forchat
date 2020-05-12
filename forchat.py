import threading
import os
import time
import datetime
import requests
import itchat
from itchat.content import PICTURE, RECORDING, ATTACHMENT, VIDEO
from lxml import etree
import pymysql
from ftplib import FTP
from youdao import get_data


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    filedpx = r'C:\Users\Administrator\Desktop\微信文件' + '\\' + msg["FileName"]
    msg.download(filedpx)
    if itchat.search_friends(userName=msg['FromUserName'])['NickName'] != itchat.search_friends()['NickName']:
        print('收到' + itchat.search_friends(userName=msg['FromUserName'])['NickName'] + '发来的文件：' + msg['FileName'])
    else:
        print('我发出的文件：' + msg['FileName'])
def dosth1():
    try:
        conn=pymysql.Connect(host='47.105.166.136',port=3306,user='test',passwd='123456',db='dictionary',charset='utf8')
        cur = conn.cursor()
        select = "SELECT * FROM english WHERE id >= ((SELECT MAX(id) FROM english)-(SELECT MIN(id) FROM english)) * RAND() + (SELECT MIN(id) FROM english) LIMIT 1;"
        cur.execute(select)
        line_count = cur.fetchone()
        txt=line_count[1]+"\n"+line_count[2]+"\n"+line_count[3]+"\n"+line_count[4]+"\n"+line_count[5]
        #print(txt)
        itchat.send_msg(txt, toUserName='filehelper')
        cur.close()
        conn.close()
    except:
        print("could not connect to mysql server")
def checkComputer():
    ftp=FTP()
    f=ftp.connect('111.33.43.98',21)
    if f != "220 Microsoft FTP Service":
        itchat.send("电脑已离线！",toUserName="filehelper")
def dosth():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 '
    }
    try:
        riqi_url = 'http://tools.2345.com/rili.htm'
        response = requests.get(riqi_url, headers=headers)
        html = etree.HTML(response.text)
        data1 = html.xpath('//*[@id="info_all"]/h3/text()')
        data2 = html.xpath('//*[@id="info_nong"]/text()')
        riqi_str = data1[0] + ' ' + data2[0]
        # print(riqi_str)
    except:
        riqi_str = '***没有获取到数据***'

    # 天气信息
    try:
        tianqi_url = 'http://tianqi.2345.com/ninghe/60517.htm'
        tianqi_response = requests.get(tianqi_url, headers=headers)
        tianqi_response.encoding = tianqi_response.apparent_encoding
        #print(tianqi_response.text)
        tianqi_html = etree.HTML(tianqi_response.text)
        tianqi_data1=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/b/text()')[0]
        tianqi_data2=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/font/text()')[0]
        tianqi_data3=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/text()')[0]
        tianqi_data4=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/font/text()')[1]
        tianqi_data5=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/text()')[2].strip()

        tianqi_str = '【天气信息】' + '\n' + tianqi_data1 + '\n' + tianqi_data2+ tianqi_data3+ tianqi_data4+ '\n' + tianqi_data5
        #print(tianqi_str)
    except:
        tianqi_str = '【天气信息】' + '\n' + '***没有获取到数据***'
        
    #限行信息
    xianxing_url = 'http://www.weather.com.cn/weather1d/101030700.shtml'
    xianxing_response = requests.get(xianxing_url, headers=headers)
    xianxing_response.encoding = xianxing_response.apparent_encoding
    #print(xianxing_response.text)
    xianxing_html = etree.HTML(xianxing_response.text)
    if xianxing_html.xpath('//div[@class="zs limit"]/em/text()'):
        xianxing_data=(xianxing_html.xpath('//div[@class="zs limit"]/span/text()')[0]+str(xianxing_html.xpath('//div[@class="zs limit"]/em/b[1]/text()')[0])+xianxing_html.xpath('//div[@class="zs limit"]/em/text()')[0]+str(xianxing_html.xpath('//div[@class="zs limit"]/em/b[2]/text()')[0]))
    else:
        xianxing_data = xianxing_html.xpath('//div[@class="zs limit"]/span/text()')[0]


    xianxing_str='【尾号限行】' + '\n' + xianxing_data

    try:
        ciba_url = 'http://open.iciba.com/dsapi/'
        resp = requests.get(ciba_url, headers=headers)
        ciba_data = resp.json()
        everyday_str = '【每日一句】' + '\n' + ciba_data['content'] + ciba_data['note']
    except:
        everyday_str = '【每日一句】' + '\n' + '***没有获取到数据***'
        # print(everyday_str)

    text = riqi_str + '\n' + tianqi_str + '\n' + xianxing_str + '\n' + everyday_str

    chatroomName = '禹帆物流生产沟通群'  # 群名
    chatrooms = itchat.search_chatrooms(chatroomName)
    if len(chatrooms) == 0:
        print('没有找到群聊：' + chatroomName)
        exit()
    else:
        #itchat.send_msg(text, toUserName=chatrooms[0]['UserName'])  # 发送消息
        itchat.send_msg(text, toUserName='filehelper')
def delete_word(char):
    try:
        conn=pymysql.Connect(host='47.105.166.136',port=3306,user='test',passwd='123456',db='dictionary',charset='utf8')
        cur = conn.cursor()
        cur.execute("select word from english where word='{}' limit 1;".format(char))
        u = cur.fetchone()
        # print(u)
        if u == None:
            # print("{}不存在,删除失败！".format(char))
            itchat.send_msg("{}不存在,删除失败！".format(char), toUserName='filehelper')
        else:
            select = "delete FROM english WHERE word='{}';".format(char)
            cur.execute(select)
            conn.commit()
            itchat.send_msg("已删除", toUserName='filehelper')
        cur.close()
        conn.close()
    except Exception as e:
        # print(e)
        # print("删除失败！")
        itchat.send_msg(e+"\n"+"删除失败！", toUserName='filehelper')
def add_word(char):
    conn=pymysql.Connect(host='47.105.166.136',port=3306,user='test',passwd='123456',db='dictionary',charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from english where word='%s' limit 1;"%char)
    u = cur.fetchone()
    # print(u)
    if u == None:
        paraph=get_data(char)
        word=paraph[0]
        IPA=paraph[1]
        paraphrase=paraph[2]
        example_sentence=paraph[3]+paraph[4]
        other=paraph[5]
        value=(word,IPA,paraphrase,example_sentence,other)
        sql="insert into english(word,IPA,paraphrase,example_sentence,other)values(%s,%s,%s,%s,%s)"
        cur.execute(sql,value)
        conn.commit()
        # print("已添加")
        # print(word+'\n'+IPA+'\n'+paraphrase+'\n'+example_sentence+'\n'+other)
        itchat.send_msg("已添加"+"\n"+word+'\n'+IPA+'\n'+paraphrase+'\n'+example_sentence+'\n'+other, toUserName='filehelper')
    else:
        # print(u[1]+'\n'+u[2]+'\n'+u[3]+'\n'+u[4]+'\n'+u[5])
        itchat.send_msg(u[1]+'\n'+u[2]+'\n'+u[3]+'\n'+u[4]+'\n'+u[5], toUserName='filehelper')
    cur.close()
    conn.close()
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg["ToUserName"]=="filehelper":
        if msg.text[0]+msg.text[1]+msg.text[2] == "cmd":
            os.system(msg.text[4:])
        if msg.text[0]+msg.text[1]+msg.text[2] == "del":
            char=msg.text[4:]
            # print(char)
            delete_word(char)
        if msg.text[0]+msg.text[1]+msg.text[2] == "add":
            char=msg.text[4:]
            # print(char)
            add_word(char)
def main():
    while True:
        now = datetime.datetime.now()
        if now.hour == 8 and now.minute in [30]:
            dosth()
            time.sleep(60)
        if now.hour in [9,10,11,12,13,14,15,16,17,18,19,20] and now.minute in [30]:
            dosth1()
            time.sleep(60)
        if now.hour in [21,22,23,0,1,2,3,4,5,6,7] and now.minute in [30]:
            checkComputer()
            time.sleep(60)
        if now.weekday() in [5,6]:
            if now.minute in [30]:
                checkComputer()
                time.sleep(60)

if __name__=="__main__":
    if not os.path.exists(r'C:\Users\Administrator\Desktop\微信文件'):
        os.mkdir(r'C:\Users\Administrator\Desktop\微信文件')
    itchat.auto_login(hotReload=True)
    itchat.get_chatrooms(update=True)
    threads = []
    thread1 = threading.Thread(target=main)
    thread2 = threading.Thread(target=itchat.run)
    threads.append(thread1)
    threads.append(thread2)
    for t in threads:
        t.start()

