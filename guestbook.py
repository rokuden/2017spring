# -*- coding: utf-8 -*-

import shelve
import shutil
import os
from datetime import datetime
from datetime import timedelta
from decorator import requires_auth
from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'
number = 1
today = datetime.now().strftime("%Y%m%d") #今日の日付を取得

def save_data(zokusei, title, shurui, create_at, create_hour): ##送信されたデータをリストに追加する
    y = datetime.now() + timedelta(days=-1)
    yesterday = y.strftime("%Y%m%d") #昨日の日付を取得
    path = "guestbook"+ yesterday + ".dat"
    aruka = os.path.isfile(path) #昨日の日付のついたデータファイルの有無を確認
    print aruka
    print path

    database = shelve.open(DATA_FILE) #本日のデータファイルを読み込む
    if aruka == False:
        shutil.copy2("guestbook.dat",path) #データファイルを日付をつけてコピー
        database.clear() #もとのデータファイルをクリア
    else:
        pass #そのままデータファイルを読み込む

    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']

    x = 1
    for greeting in greeting_list:
        x += 1
        print x

    greeting_list.insert(0, {
        'zokusei': zokusei,
        'title': title,
        'shurui': shurui,
        'create_at': create_at,
        'create_hour': create_hour
    })
    database['greeting_list'] = greeting_list
    database.close

def load_data(): ##データファイルを読み込んでリストを返す
    database = shelve.open(DATA_FILE)
    greeting_list = database.get('greeting_list', [])
    print DATA_FILE
    database.close()
    return greeting_list

def load_yesterday_data(): ##昨日のデータファイルを読み込んでリストを返す
    y = datetime.now() + timedelta(days=-1)
    yesterday = y.strftime("%Y%m%d") #昨日の日付を取得
    YESTERDAY_DATA_FILE = "guestbook" + yesterday + ".dat"
    database = shelve.open(YESTERDAY_DATA_FILE)
    print YESTERDAY_DATA_FILE
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list

def load_ototoi_data(): ##一昨日のデータファイルを読み込んでリストを返す
    o = datetime.now() + timedelta(days=-2)
    ototoi = o.strftime("%Y%m%d")
    OTOTOI_DATA_FILE = "guestbook" + ototoi + ".dat"
    database = shelve.open(OTOTOI_DATA_FILE)
    print OTOTOI_DATA_FILE
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list

@application.before_request ##すべてのページにBasic認証をかける 
@requires_auth
def before_request():
    pass

@application.route('/today') ##リストを読んでレンダリングする
def index():
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)

@application.route('/yesterday') ##昨日のリストを読んでレンダリングする
def yesterday_index():
    greeting_list = load_yesterday_data()
    return render_template('index.html', greeting_list=greeting_list)

@application.route('/ototoi') ##一昨日のリストを読んでレンダリングする
def ototoi_index():
    greeting_list = load_ototoi_data()
    return render_template('index.html', greeting_list=greeting_list)

@application.route('/past/<how_past>') ##過去のデータファイルからリストを読んでレンダリングする
def past_index(how_past):
    how_past = int(how_past)
    p = datetime.now() - timedelta(days=how_past )
    past = p.strftime("%Y%m%d")
    PAST_DATA_FILE = "guestbook" + past + ".dat"
    database = shelve.open(PAST_DATA_FILE)
    print PAST_DATA_FILE
    greeting_list = database.get('greeting_list', [])
    database.close()
    return render_template('index.html', greeting_list=greeting_list)

@application.route('/post', methods=['POST']) ##index.htmlから入力したデータをpostして送信する
def post():
    zokusei = request.form.get('zokusei') #フォームから属性を取得
    title = request.form.get('title') #フォームからタイトルを取得
    shurui = request.form.get('shurui') #フォームから種類を取得
    create_at = datetime.now() #フォームに入力された日時を取得
    create_hour = request.form.get('create_hour') #フォームに入力された時間を取得

    now_hour = datetime.now().strftime("%H") #現在時間を取得

    if create_hour == 'now':
        create_hour = now_hour #取得した時間を代入
    else:
        pass

    create_hour = int(create_hour) #create_hourをstr型からint型に変換

    save_data(zokusei, title, shurui, create_at, create_hour)

    return redirect('/today')

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
