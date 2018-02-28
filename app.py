import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']

def apple_news():
    target_url = 'http://www.appledaily.com.tw/realtimenews/section/new/'
    head = 'https://www.appledaily.com.tw'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 8:
            return content
        meta = data.find("font")
        title = meta.text
        link = data['href']
        '''if head in data['href']:
            link = data['href']
        else:
            link = head + data['href']'''
        content += '{}\n{}\n\n'.format(title,link)
    return content

def bbc_news():
    url = 'http://www.bbc.com/news'
    head = 'http://www.bbc.com'
    print('Start parsing bbc_news')
    rs = requests.session()
    res = rs.get(url,verify=False)
    sp = BeautifulSoup(res.text,'html.parser')
    content = ""
    datamain = sp.select('.nw-c-most-read__items')
    meta = datamain[0].find_all('a',{'class':'gs-c-promo-heading'})
    for titles in meta:
        link = titles['href']
        title = titles.find('span',{'class':'gs-c-promo-heading__title'}).text
        link = head+link
        content += '{}\n{}\n\n'.format(title,link)
    return content

def movie():
    url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie')
    rs = requests.session()
    res = rs.get(url,verify=False)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    content = ""
    for index,data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t','').replace('\r','')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n\n'.format(title,link)
    return content

def bitcoin_news():
    url = 'https://www.wantgoo.com/global/stockindex?stockno=bitcoin'
    rs = requests.session()
    res = rs.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    maindata = soup.select('div.idx-quotes.clearfix')
    prices = soup.select('div.idx-data b.i')
    main = maindata[0].find('span',{'class':'price'}).text
    value = []
    for price in prices :
        value.append(price)
    content = "<bitcoin>\n即實行情 : {}\n開盤 : {}\n 最高 : {}\n 最低 : {}\n 昨收 : {}\n 成交量 : {}\n".format(main,value[0].text,value[1].text,value[2].text,value[3].text,value[4].text)
    return content

def lottery_news():
    url = 'http://www.taiwanlottery.com.tw/index_new.aspx'
    rs = requests.session()
    res = rs.get(url,verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    content = ""
    maincolumn = soup.select('#rightdown')
    #威力彩
    meta = maincolumn[0].find_all('div',{'class':'contents_box02'})
    data1_1 = meta[0].find_all('div',{'class':'ball_tx'})
    data1_2 = meta[0].find('div',{'class':'ball_red'})
    date = meta[0].find('span',{'class':'font_black15'}).text
    content += "威力彩 "+date+"\n"
    for n in range(6,len(data1_1)):
        content += data1_1[n].text+" "
    content += "\n"+data1_2.text+"\n"
    #大樂透
    data2_1 = meta[2].find_all('div',{'class':'ball_tx'})
    data2_2 = meta[2].find('div',{'class':'ball_red'})
    date = meta[2].find('span',{'class':'font_black15'}).text
    content += "大樂透 "+date+"\n"
    for n in range(7,len(data2_1)):
        content += data2_1[n].text+" "
    content += "\n"+data2_2.text+"\n"
    #大福彩
    meta = maincolumn[0].find('div',{'class':'contents_box05'})
    data3_1 = meta.find_all('div',{'class':'ball_tx'})
    data3_2 = meta.find('div',{'class':'ball_red'})
    date = meta.find('span',{'class':'font_black15'}).text
    content += "大福彩 "+date+"\n"
    for n in range(7,len(data3_1)):
        content += data3_1[n].text+" "
    content += "\n"+data3_2.text+"\n"
    #今彩539
    meta = maincolumn[0].find('div',{'class':'contents_box03'})
    data4_1 = meta.find_all('div',{'class':'ball_tx'})
    date = meta.find('span',{'class':'font_black15'}).text
    content += "今彩539 "+date+"\n"
    for n in range(6,len(data4_1)):
        content += data4_1[n].text+" "
    content += "\n"
    #三星彩
    meta = maincolumn[0].find_all('div',{'class':'contents_box04'})
    data5_1 = meta[0].find_all('div',{'class':'ball_tx'})
    date = meta[0].find('span',{'class':'font_black15'}).text
    content += "三星彩 "+date+"\n"
    for n in range(0,len(data5_1)):
        content += data5_1[n].text+" "
    content += "\n"
    #四星彩
    meta = maincolumn[0].find_all('div',{'class':'contents_box04'})
    data6_1 = meta[1].find_all('div',{'class':'ball_tx'})
    date = meta[0].find('span',{'class':'font_black15'}).text
    content += "四星彩 "+date+"\n"
    for n in range(0,len(data6_1)):
        content += data6_1[n].text+" "
    content += "\n"
    return content
    
def ptt_hot():
    url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(url,verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    content = ""
    data = soup.select('#list div.row2 span.L34.nowrap.listTitle')
    for head in data:
        title = head.text
        link = "http://disp.cc/b/"+head.find('a')['href']
        if head.find('a')['href'] == "796-5919":
            break
        content += '{}\n{}\n\n'.format(title,link) 
    return content  

def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index+5:end_index]
    return int(page_number)

def craw_page(res,push_rate):
    soup_ = BeautifulSoup(res.text,'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            link = r_ent.find('a')['href']
            if link:
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate :
                    rate = 100 if str(rate).startswith('爆') else rate
                    rate = -1 * int(rate[1]) if str(rate).startswith('X') else rate
                else:
                    rate = 0
                if int(rate) >= push_rate:
                    article_seq.append({'title':title,'url':url,'rate':rate},)
        except Exception as e:
            print("本文已刪除")
    return article_seq

def ptt_beauty():
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    rs = requests.session()
    res = rs.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2
    push_rate = 10
    index_list = []
    article_list = []
    for page in range(start_page,start_page-page_term,-1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    while index_list:
        index = index_list.pop(0)
        res = rs.get(index,verify=False)
        if res.status_code != 200:
            index_list.append(index)
        else:
            for element in craw_page(res,push_rate):
                article_list.append(element)
    content = ""
    for article in article_list:
        data = '[{} push ] {}\n{}\n\n'.format(article.get('rate',None),article.get('title',None),article.get('url',None))
        content += data
    return content

def books_topsale():
    url = 'http://www.books.com.tw/web/sys_saletopb/books'
    rs = requests.session()
    res = rs.get(url,verify=False)
    soup = BeautifulSoup(res.text,'html.parser')

    data = soup.select('li.item div.type02_bd-a')
    top20_data = []
    content = ""

    for index,head in enumerate(data[0:20],1):
        no = index
        title = head.find("a").text
        href = head.find("a")['href']
        top20_data.append({'no':no,'title':title,'href':href})
    for article in top20_data:
        meta = '[top {}] {}\n{}\n\n'.format(article.get('no',None),article.get('title',None),article.get('href',None))
        content += meta
    return content

def books_topnew():
    url = 'http://www.books.com.tw/web/sys_newtopb/books'
    rs = requests.session()
    res = rs.get(url,verify=False)
    soup = BeautifulSoup(res.text,'html.parser')

    data = soup.select('li.item div.type02_bd-a')
    top10_data = [] 
    content = ""

    for index,head in enumerate(data[0:10],1):
        no = index
        title = head.find("a").text
        href = head.find("a")['href']
        top10_data.append({'no':no,'title':title,'href':href})
    for article in top10_data:
        meta = '[top {}] {}\n{}\n\n'.format(article.get('no',None),article.get('title',None),article.get('href',None))
        content += meta
    return content

def air_news():
    url = "https://taqm.epa.gov.tw/taqm/tw/Aqi/North.aspx?fm=AqiMap"
    info = "AQI\n0~50 良好\n51~100 普通\n101~150 對敏感族群不健康\n151~200 對所有族群不健康\n201-300 非常不健康\n301-400 危害\n401-500 危害\n\n"
    rs = requests.session()
    res = rs.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    table1 = soup.select('#ctl09_UpdatePanel1 table.TABLE_G')
    table2 = soup.select('#ctl09_UpdatePanel2 table.TABLE_G')
    station_list = []
    content = ""
    content += info

    for index,station in enumerate(table1[0].select('tr[style="color:Black;"]'),2):
        if index < 10:
            try:
                id_name = "ctl09_gv_ctl0{}_linkSite".format(index)
                aqi_name ="ctl09_gv_ctl0{}_labPSI".format(index)
                name = station.find("a",id=id_name).text
                aqi = station.find("span",id=aqi_name).text
                station_list.append({'name':name,'aqi':aqi})
            except Exception as e:
                print(e)
        else:
            try:
                id_name = "ctl09_gv_ctl{}_linkSite".format(index)
                aqi_name = "ctl09_gv_ctl{}_labPSI".format(index)
                name = station.find("a",id=id_name).text
                aqi = station.find("span",id=aqi_name).text
                station_list.append({'name':name,'aqi':aqi})
            except Exception as e:
                print(e)
    for index,station in enumerate(table2[0].select('tr[style="color:Black;"]'),2):
        if index < 10:
            try:
                id_name = "ctl09_gv2_ctl0{}_linkSite".format(index)
                aqi_name = "ctl09_gv2_ctl0{}_labPSI".format(index)
                name = station.find("a",id=id_name).text
                aqi = station.find("span",id=aqi_name).text
                station_list.append({'name':name,'aqi':aqi})
            except Exception as e:
                print(e)
        else:
            try:
                id_name = "ctl09_gv2_ctl{}_linkSite".format(index)
                aqi_name = "ctl09_gv2_ctl{}_labPSI".format(index)
                name = station.find("a",id=id_name).text
                sqi = station.find("span",id=aqi_name).text
                station_list.append({'name':name,'aqi':aqi})
            except Exception as e:
                print(e)
    for article in station_list:
        meta = "{} {}\n".format(article.get('name',None),article.get('aqi',None))
        content += meta
    return content

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "bbc":
        content = bbc_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "最新電影":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "bitcoin":
        content = bitcoin_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "樂透":
        content = lottery_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "ptt":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "ptt表特":
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "book暢銷":
        content = books_topsale()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "book新書":
        content = books_topnew()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "空汙":
        content = air_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "friend":
        client = ImgurClient(client_id,client_secret)
        print(client)
        print(client_id)
        print(client_secret)
        print(album_id)
        images = client.get_album_images(album_id)
        index = random.randint(0,len(images)-1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token,image_message)
        return 0 
    if event.message.text == "你是誰":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="chatbot聊天機器人"))
        return 0
    if event.message.text == "簡介":
        content = 'chat bot 指令功能\n"空汙"->即時空氣品質\n"bitcoin"->即時比特幣價格\n"book暢銷"->博客來即時暢銷書單top20\n"book新書"->博客來新書書單top10\n"樂透"->樂透最新開獎號碼\n"最新電影"->最新已上映電影\n"bbc"->bbc熱門新聞top10\n"ptt"->ptt熱門文章\n"'
        line_bot_api.reply_message(
            event.reply_token,
            TestSendMessage(text=content))
    

if __name__ == '__main__':
    app.run()
