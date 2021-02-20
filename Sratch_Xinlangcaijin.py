
import os
import datetime
import time
import requests
from lxml import etree
import re


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
    txtname = 'hotnews.txt'
    today = str(datetime.date.today())
    my_date = today.replace("-","")
    #print(my_date)
    #以下网址为新浪统计点击量的地址
    url0 = "http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_0_suda&top_time="+my_date+"&top_show_num=20&top_order=DESC&js_var=all_1_data&get_new=1" #总榜，可在此修改条数
    url1 = "http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_news_0_suda&top_time="+my_date+"&get_new=1&top_show_num=20&top_order=DESC&js_var=all_1_data" #新闻榜，可在此修改条数
    url2 = "http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_not_url=/ustock/&top_type=day&top_cat=finance_stock_conten_suda&top_time="+my_date+"&top_show_num=20&top_order=DESC&get_new=1&js_var=stock_1_data" #证券榜，可在此修改条数
    url3 = "http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_money_suda&top_time="+my_date+"&top_show_num=20&top_order=DESC&get_new=1&js_var=money_1_data" #理财榜，可在此修改条数

    if (os.path.exists(txtname)):
        os.remove(txtname) #删除上一次抓取的文件

    href_list0 = get_topnews_url(url=url0)  #总榜
    href_list1 = get_topnews_url(url=url1)  #新闻榜
    href_list2 = get_topnews_url(url=url2)  #股票榜
    #print(href_list0)
    #href_list = extract_url(url=url)
    #print(href_list)
    for href in href_list2:
        # 排除非新浪连接
        print(href)
        if href.startswith("https://finance.sina.com.cn/roll") or href.startswith("https://finance.sina.com.cn/stock") :
            try:
                html = search_article(href)
                article = parse_html(html)
                write_article(article)
            except Exception as e:
                print(e)



