#!/usr/bin/python

#encoding=utf-8
import tushare,time

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

def main(sharelist):
    # share = Share(code)
    for share in sharelist:
        sss=getrealtimedata(share)
        print(sss.describe)

        if sss.price <=sss.buy:
            print('价格超低，赶紧买入！')
        elif sss.price >= sss.sale:
            print('赶紧卖出。大赚了！')
        else:
            print('静观其变……')

if __name__=="__main__":
    while True:
        share1=Share("603697",18.7,100.0)
        share2=Share("002310",18.7,200.0)
        share3=Share("000591",18.7,300.0)
        sharelist = [share1,share2,share3]
        main(sharelist)
        time.sleep(5)
