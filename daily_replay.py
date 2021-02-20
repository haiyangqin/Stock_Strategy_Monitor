
import os
import datetime
import tushare,time
import requests
from lxml import etree
import re

def getrealtimedata(share):
    data = tushare.get_realtime_quotes(share.code)
    share.name = data.loc[0][0]
    share.open = float(data.loc[0][1])
    share.price = float(data.loc[0][3])
    share.high = float(data.loc[0][4])
    share.low = float(data.loc[0][5])
    share.describe='股票编号：{}，股票名称：{}，今日开盘价：{}，当前价格：{}，今日最高价：{}，今日最低价：{}'.format(share.code,share.name,share.open,share.price,share.high,share.low)
    return share

class Share():
    def __init__(self,code,buy,sale):
        self.name = ''
        self.open = ''
        self.price = ''
        self.high = ''
        self.low = ''
        self.describe=''
        self.code = code
        self.buy = buy
        self.sale = sale

def search_article(url):
    """
    请求所传的url
    args：
        url: 所要请求的url
    return:
        类lxml.etree._Element的元素, 可以直接用xpath解析
    """

    header = {
        'Accept': '*/*',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/66.0.3359.181 Safari/537.36'
    }
    resp = requests.get(url, headers=header)
    #print(resp)
    html_str = str(resp.content, 'utf-8')
    #print(html_str)
    selector = etree.HTML(html_str)
    #print(selector)
    return selector

def get_topnews_url(url):
    """
    请求所传的url
    args：
        url: 所要请求的url
    return:
        类lxml.etree._Element的元素, 可以直接用xpath解析
    """

    header = {
        'Accept': '*/*',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/66.0.3359.181 Safari/537.36'
    }
    resp = requests.get(url, headers=header)
    #print(resp)
    html_str = str(resp.content, 'utf-8')#以字符串形式返回网页内容
    url_list = html_str.replace('\\','')#删除里面的\\符
    url_list = re.findall(r'url":"([^"]+)"',url_list)#提取里面url":"后面的链接

    #print(html_str)
    #selector = etree.HTML(html_str)
    #print(selector)
    return url_list

def parse_html(selector):
    """
    解析提取的lxml.etree._Element的元素
    return:
        type:dict
            key:news title
            value: contents of news
    """
    try:
        title_text = selector.xpath('//h1/text()')[0]
        # 获取class=article的div下面的p标签的所有text()
        article_text = selector.xpath('//div[@class="article"]/p//text()')

        return {title_text: article_text}
    except Exception as e:
        return {'解析错误': [e]}


def write_article(article):
    """
    将所传的新闻字典写入文件news.txt中
    args：
        article：dict {news_title:[contents,]}
    No return
    """
    file_name = txtname
    f = open(file_name, 'a', encoding='utf-8')
    title = list(article.keys())[0]
    f.write("(●'◡'●)："+title + '\n')
    #for content in article[title]: #只要标题，不要内容
    #    f.write(content+"\n")
    f.write("\n\n")
    f.close()


def extract_url(url):
    #print(search_article(url))
    href_lists = search_article(url).xpath("//div[@id='fin_tabs0_c0']//a//@href")
    return href_lists


if __name__ == '__main__':
    today_date = datetime.date.today()
    last_month_start = datetime.date(today_date.year, today_date.month-1, 1)
    today_date = str(today_date)
    last_month_start = str(last_month_start)

    #print(today_date)
    #print(last_month_start)

    #tushare.set_token('132d6a8cdca70dbad80a0f97a33c8c3e410e71215843ced80eb6d6f9')
    #pro=tushare.pro_api('132d6a8cdca70dbad80a0f97a33c8c3e410e71215843ced80eb6d6f9')

    shzs =  tushare.get_hist_data('sh',start=last_month_start,end=today_date)
    szzs =  tushare.get_hist_data('sz',start=last_month_start,end=today_date)
    cybzs = tushare.get_hist_data('cyb',start=last_month_start,end=today_date)
    kcbzs = tushare.get_hist_data('kcb',start=last_month_start,end=today_date)

    #pro.moneyflow_hsgt()

    #sh_rqye = tushare.sh_margins(start=last_month_start,end=today_date)
    #sz_rqye = tushare.sz_margins(start=last_month_start,end=today_date)

    #昨日情况
    sh_sz_all_vol    = round(shzs.volume[1]/1000000 + szzs.volume[1]/100000000,2)              #两市昨日成交总量
    sh_vol_rate      = "%.2f%%" % ((shzs.volume[1] - shzs.volume[2])/shzs.volume[2] * 100)     #上证昨日成交量变化
    sz_vol_rate      = "%.2f%%" % ((szzs.volume[1] - szzs.volume[2])/szzs.volume[2] * 100)     #深证昨日成交量变化
    cyb_vol_rate     = "%.2f%%" % ((cybzs.volume[1] - cybzs.volume[2])/cybzs.volume[2] * 100)  #创业板昨日成交量变化
    #kcbzs_vol_rate   = "%.2f%%" % ((kcbzs.volume[1] - kcbzs.volume[2])/kcbzs.volume[2] * 100) #科创板指数昨日成交量变化

    print(sh_sz_all_vol)
    print(sh_vol_rate)
    print(sz_vol_rate)
    print(cyb_vol_rate)
    #print(kcbzs_vol_rate)

    #print(shzs.volume[1])
    #print(szzs.volume[1])
    #print(cybzs.volume)
    #print(kcbzs.volume)

    #今日情况
    sh_change  = "%.2f%%" %(shzs.p_change[0])
    sz_change  = "%.2f%%" %(szzs.p_change[0])
    cyb_change = "%.2f%%" %(cybzs.p_change[0])

    print(sh_change)
    print(sz_change)
    print(cyb_change)

    file_name = 'daily_replay.txt'
    if (os.path.exists(file_name)):
        os.remove(file_name) #删除上一次抓取的文件
    f = open(file_name, 'a', encoding='utf-8')
    # 判断日期是否是交易日
    trade_date = datetime.date.today()
    trade_date = trade_date + datetime.timedelta(days=-1)
    #print(trade_date)
    f.write(str(trade_date)+"复盘|\n\n")
    f.write("昨日 --> \n")
    f.write("两市成交总量： "+str(sh_sz_all_vol)+"亿\n")
    if((shzs.volume[1] - shzs.volume[2]) > 0):
      arrow = " ⬆"
    else:
      arrow = " ⬇"
    f.write("上证指数成量变化： "+str(sh_vol_rate)+arrow+"\n")
    if ((szzs.volume[1] - szzs.volume[2]) > 0):
        arrow = " ⬆"
    else:
        arrow = " ⬇"
    f.write("深成指成量变化： "+str(sz_vol_rate)+arrow+"\n")
    if ((cybzs.volume[1] - cybzs.volume[2]) > 0):
        arrow = " ⬆"
    else:
        arrow = " ⬇"
    f.write("创业板成量变化： "+str(cyb_vol_rate)+arrow+"\n")
    f.write("融券余额：      \n")
    f.write("北上资金：      \n")
    f.write("资金流入板块：   \n\n")
    f.write("今日 --> \n")
    f.write("上涨指数:    "+str(sh_change)+"\n")
    f.write("深成指数:    "+str(sz_change)+"\n")
    f.write("创业板指数:  "+str(cyb_change)+"\n")
    f.write("活跃板块：      \n")

    #for content in article[title]: #只要标题，不要内容
    #    f.write(content+"\n")
    f.write("\n\n")
    f.close()

