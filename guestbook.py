# -*- coding: utf-8 -*-

import shelve
import shutil
import os
import sys
import codecs
from datetime import datetime
from datetime import timedelta
from decorator import requires_auth
from flask import Flask, request, render_template, redirect, escape, Markup

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
application = Flask(__name__)

#DATA_FILE = 'guestbook.dat'
ACCESS_COUNTER = 'access.dat'
today = datetime.now().strftime("%Y%m%d") #今日の日付を取得
today_time = datetime.now().strftime("%Y%m%d%H%M")

class MyDatabase:
    def __init__(self, fpath):
        self.db = shelve.open(fpath)

    def create(self, value):
        idx = self.db.keys()
        if len(idx) == 0:
            idx = [0]

        idx = map(int, idx)
        idx_int = int(max(idx)) + 1
        idx = str(idx_int)

        self.db[idx] = value

    def delete(self, idx):
        idx = str(idx)
        if idx in self.db:
            del self.db[idx]

mydb = MyDatabase("task_list.shelve")

def save_data(zokusei, title, shurui, create_at, create_hour): ##送信されたデータをリストに追加する

    mydb = MyDatabase("task_list.shelve")

    y = datetime.now() + timedelta(days=-1)
    yesterday = y.strftime("%Y%m%d") #昨日の日付を取得
    path = "task_list"+ yesterday + ".shelve"
    aruka = os.path.isfile(path) #昨日の日付のついたデータファイルの有無を確認
    print aruka
    print path
    if aruka == False:
        shutil.copy2("task_list.shelve",path) #データファイルを日付をつけてコピー
        mydb.db.clear() #もとのデータファイルをクリア
        print "data copied and today's data was initialized"

    mydb.create({
        'zokusei': zokusei,
        'title': title,
        'shurui': shurui,
        'create_at': create_at,
        'create_hour': create_hour
    })
    mydb.db.close()

def load_data(): ##データファイルを読み込んでリストを返す

    mydb = MyDatabase("task_list.shelve")
    y = datetime.now() + timedelta(days=-1)
    yesterday = y.strftime("%Y%m%d") #昨日の日付を取得
    path = "task_list"+ yesterday + ".shelve"
    aruka = os.path.isfile(path) #昨日の日付のついたデータファイルの有無を確認
    print aruka
    print path
    if aruka == False:
        shutil.copy2("task_list.shelve",path) #データファイルを日付をつけてコピー
        mydb.db.clear() #もとのデータファイルをクリア
        print "data copied and today's data was initialized"
    

    list_keys = mydb.db.keys()
    #print list_keys


    """for i in list_keys:
        print i
        print mydb.db[str(i)]['shurui']
        print mydb.db[str(i)]['create_hour']"""

    tb = u"<table id='pukopuko' border='1'><tr><th>時間,属性</th>"
    for n in range(1, 25):
       tb+="<td>" + str(n) + ":00" + "</td>"
    tb+= "</tr>"
    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'otto':
            tb+=u"<tr bgcolor='#c1e4e9'><th>夫</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'tuma':
            tb+=u"<tr bgcolor='#eebbcb'><th>妻</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'chonan':
            tb+= u"<tr bgcolor='#dccb18'><th>長男</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'jinan':
            tb+= u"<tr bgcolor='#a59aca'><th>次男</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"
    
    tb+="</table>"
    
    mydb.db.close()


    access = shelve.open(ACCESS_COUNTER, writeback=True)#アクセス記録
    if 'counter' not in access:
        access['counter'] = [today_time]
    else:
        #print access['counter']

        access['counter'].append(today_time)

    access.close() #ここまで

    #return counter
    #itsu = "今日"

    return tb

def load_data_task():

    mydb = MyDatabase("task_list.shelve")
    list_keys = mydb.db.keys()
    print list_keys
    
    tc = u"<table id='pikopiko' border='1'><tr><th>時間,種類</th><th>タイトル</th>"
    for n in range(1, 25):
       tc+="<td>" + str(n) + ":00" + "</td>"
    tc+= "</tr>"
    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'jibun':
            tc+=u"<tr bgcolor='#c49a6a'><th>自分のため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else: #取らないで
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'dareka':
            tc+=u"<tr bgcolor='#79c06e'><th>家族の誰かのため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else:
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'zennin':
            tc+= u"<tr bgcolor='#4496d3'><th>家族全員のため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else:
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'shakai':
            tc+= u"<tr bgcolor='#e95388'><th>社会のため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else:
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"
    tc+="</table>"

    #print tc
    mydb.db.close()
    return tc

def load_data_past(past): ##データファイルを読み込んでリストを返す
    
    mydb = MyDatabase("task_list" + past + ".shelve")
    list_keys = mydb.db.keys()
    #print list_keys

    tb = u"<table id='pukopuko' border='1'><tr><th>時間,属性</th>"
    for n in range(1, 25):
       tb+="<td>" + str(n) + ":00" + "</td>"
    tb+= "</tr>"
    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'otto':
            tb+=u"<tr bgcolor='#c1e4e9'><th>夫</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'tuma':
            tb+=u"<tr bgcolor='#eebbcb'><th>妻</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'chonan':
            tb+= u"<tr bgcolor='#dccb18'><th>長男</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['zokusei'] == 'jinan':
            tb+= u"<tr bgcolor='#a59aca'><th>次男</th>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['shurui'] == 'jibun':
                        tb+= "<td bgcolor='#c49a6a'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'dareka':
                        tb+= "<td bgcolor='#79c06e'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'zennin':
                        tb+= "<td bgcolor='#4496d3'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    elif mydb.db[str(i)]['shurui'] == 'shakai':
                        tb+= "<td bgcolor='#e95388'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                    else:
                        tb+= "<td bgcolor='#afafb0'>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
                else:
                    tb+= "<td>&nbsp;</td>"
            tb+="</tr>"
    
    tb+="</table>"
    
    mydb.db.close()
    return tb

def load_data_task_past(past):

    mydb = MyDatabase("task_list" + past + ".shelve")
    list_keys = mydb.db.keys()
    #print list_keys
    
    tc = u"<table id='pikopiko' border='1'><tr><th>時間,種類</th><th>タイトル</th>"
    for n in range(1, 25):
       tc+="<td>" + str(n) + ":00" + "</td>"
    tc+= "</tr>"
    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'jibun':
            tc+=u"<tr bgcolor='#c49a6a'><th>自分のため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else: #取らないで
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'dareka':
            tc+=u"<tr bgcolor='#79c06e'><th>家族の誰かのため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else:
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'zennin':
            tc+= u"<tr bgcolor='#4496d3'><th>家族全員のため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else:
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"

    for i in list_keys:
        if mydb.db[str(i)]['shurui'] == 'shakai':
            tc+= u"<tr bgcolor='#e95388'><th>社会のため</th>"
            tc+="<td>" + "(" + str(i) + ")" + mydb.db[str(i)][u'title'] + "</td>"
            for n in range(1, 25):
                if str(n) == str(mydb.db[str(i)]['create_hour']):
                    if mydb.db[str(i)]['zokusei'] == 'otto':
                        tc+= u"<td bgcolor='#c1e4e9'>夫</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'tuma':
                        tc+= u"<td bgcolor='#eebbcb'>妻</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'chonan':
                        tc+= u"<td bgcolor='#dccb18'>長男</td>"
                    elif mydb.db[str(i)]['zokusei'] == 'jinan':
                        tc+= u"<td bgcolor='#a59aca'>次男</td>"
                else:
                    tc+= "<td>&nbsp;</td>"
            tc+="</tr>"
    tc+="</table>"
    
    mydb.db.close()
    return tc

def del_gamen():
    mydb = MyDatabase("task_list.shelve")
    list_keys = mydb.db.keys()
    dele = u"<table border='1'><tr><td>番号</td><td>属性</td><td>タイトル</td><td>削除ボタン</td></tr>"
    for i in list_keys:
        dele+= "<tr>"
        dele+= "<td>" + i + "</td>"
        if mydb.db[str(i)]['zokusei'] == 'otto':
            dele+= u"<td bgcolor='#c1e4e9'>夫</td>"
        elif mydb.db[str(i)]['zokusei'] == 'tuma':
            dele+= u"<td bgcolor='#eebbcb'>妻</td>"
        elif mydb.db[str(i)]['zokusei'] == 'chonan':
            dele+= u"<td bgcolor='#dccb18'>長男</td>"
        elif mydb.db[str(i)]['zokusei'] == 'jinan':
            dele+= u"<td bgcolor='#a59aca'>次男</td>"
        dele+= "<td>" + mydb.db[str(i)][u'title'] + "</td>"
        dele+= """<td><button type='button' onclick="location.href='/all/""" + i + """'">"""
        dele+= u"削除する</button></form></td>"
        dele+= "</tr>"

    dele+= "</table>"

    mydb.db.close()
    return dele

def del_gamen_past(past, how_past):
    mydb = MyDatabase("task_list" + past + ".shelve")
    list_keys = mydb.db.keys()
    dele = u"<table border='1'><tr><td>番号</td><td>属性</td><td>タイトル</td><td>削除ボタン</td></tr>"
    for i in list_keys:
        dele+= "<tr>"
        dele+= "<td>" + i + "</td>"
        if mydb.db[str(i)]['zokusei'] == 'otto':
            dele+= u"<td bgcolor='#c1e4e9'>夫</td>"
        elif mydb.db[str(i)]['zokusei'] == 'tuma':
            dele+= u"<td bgcolor='#eebbcb'>妻</td>"
        elif mydb.db[str(i)]['zokusei'] == 'chonan':
            dele+= u"<td bgcolor='#dccb18'>長男</td>"
        elif mydb.db[str(i)]['zokusei'] == 'jinan':
            dele+= u"<td bgcolor='#a59aca'>次男</td>"
        dele+= "<td>" + mydb.db[str(i)][u'title'] + "</td>"
        dele+= """<td><button type='button' onclick="location.href='/all/""" + str(how_past) + "/"+ i + """'">"""
        dele+= u"削除する</button></form></td>"
        dele+= "</tr>"

    dele+= "</table>"

    mydb.db.close()
    return dele

def del_data_past(past, kore):
    mydb = MyDatabase("task_list" + past + ".shelve")
    mydb.delete(kore)
    mydb.db.close()


def del_data(kore):
    mydb = MyDatabase("task_list.shelve")
    mydb.delete(kore)
    mydb.db.close()

@application.before_request ##すべてのページにBasic認証をかける
@requires_auth
def before_request():
    pass

@application.route('/touroku') ##登録画面
def touroku():
    return render_template('touroku.html')

@application.route('/all') ##項目削除ページ
def del_del():
    dele = del_gamen()
    return render_template('delete.html',dele=dele)

@application.route('/all/<dore>') ##削除しよう
def del_poko(dore):
    kore = dore
    del_data(kore)
    return redirect('/all')

@application.route('/all/past/<how_past>') ##かこの項目削除ページ
def del_del_past(how_past):
    how_past = int(how_past)
    p = datetime.now() - timedelta(days=how_past )
    past = p.strftime("%Y%m%d")
    dele = del_gamen_past(past, how_past)
    return render_template('delete.html',dele=dele)

@application.route('/all/<how_past>/<dore>') ##過去を削除しよう
def del_poko_past(how_past, dore):
    kore = dore
    how_past = int(how_past)
    p = datetime.now() - timedelta(days=how_past )
    past = p.strftime("%Y%m%d")
    del_data_past(past,kore)
    return redirect('/all/' + str(how_past))

@application.route('/today') ##リストを読んでレンダリングする
def index():
    tb = load_data()
    tc = load_data_task()
    return render_template('index.html', tb=tb, tc=tc)

@application.route('/past/<how_past>') ##過去のデータファイルからリストを読んでレンダリングする
def past_index(how_past):
    
    how_past = int(how_past)
    p = datetime.now() - timedelta(days=how_past )
    past = p.strftime("%Y%m%d")

    tb = load_data_past(past)
    tc = load_data_task_past(past)
    #itsu = str(how_past) + "日前"
    return render_template('index.html', tb=tb,tc=tc)
    #return rendddr_template('index.html', itsu)
    

@application.route('/post', methods=['POST']) ##index.htmlから入力したデータをpostして送信する
def post():
    zokusei = request.form.get('zokusei') #フォームから属性を取得
    title = request.form.get('title') #フォームからタイトルを取得
    shurui = request.form.get('shurui') #フォームから種類を取得
    create_at =  datetime.now().strftime("%Y%m%d%H%M%S")#フォームに入力された日時を取得
    create_hour = request.form.get('create_hour') #フォームに入力された時間を取得

    now_hour = datetime.now().strftime("%H") #現在時間を取得

    if create_hour == 'now':
        create_hour = now_hour #取得した時間を代入
    else:
        pass

    create_hour = int(create_hour) #create_hourをstr型からint型に変換

    save_data(zokusei, title, shurui, create_at, create_hour)

    return redirect('/touroku')

@application.template_filter('n12br') ##改行文字をbrにする
def n12br_filter(s):
    return escape(s).replace('\n', Markup('<br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')

@application.template_filter('hour_fmt')
def hour_fmt_filter(dt):
    return int(dt.strftime('%H'))

@application.template_filter('date_fmt')
def date_fmt_filter(dt):
    return int(dt.strftime('%d'))

@application.template_filter('year_hour_date_fmt')
def date_time_fmt_filter(dt):
    return int(dt.strftime('%Y'+'%m'+'%d'))

if __name__ == '__main__':
    application.run('127.0.0.1', 5000, debug=True)
