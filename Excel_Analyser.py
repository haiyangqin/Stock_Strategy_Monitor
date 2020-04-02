#!/usr/bin/python

#encoding=utf-8
import xlrd
import Stock_Monitor
import Files_EmailSender

class excel_analyser(object):

    def zs_wg_analyse(self,xl_name):
        '''
        中枢 网格 表
        xl_name: 表格名称
        '''
        xl_opened = xlrd.open_workbook(xl_name)
        table = xl_opened.sheets()[0]
        rows_num = table.nrows
        cols_num = table.ncols
        #print(rows_num)
        #print(cols_num)
        for i in range(rows_num):
            #print(table.cell_value(i,0))
            if '交易品种' in table.cell_value(i,0):
                content= table.cell_value(i,1)
                stock_name = content.split('（')[0] #股票名称
                stock_id = content.split('（')[1].split('）')[0] #股票代码
                temp = Stock_Monitor.Share(stock_id,0,0)
                geted_info = Stock_Monitor.getrealtimedata(temp)
                geted_stock_name = geted_info.describe.split('股票名称：')[1].split('，')[0]
                if(geted_stock_name != stock_name):
                   print('股票名称和代码不对应，请检查excel表格！')
                   print('geted_stock_name:'+geted_stock_name+' '+'expected_stock_name:'+stock_name)
                   err_senders0 = Files_EmailSender.Carry_files_EmailSender()
                   err_senders0.send_email(["420195048@qq.com"], "ERR: 股票名称和代码不对应 @Strategy Monitor", "股票名称和代码不对应: "+stock_name+stock_id,"")
                current_stock_price = geted_info.price
            #处理日线级别中枢
            if '1D' in table.cell_value(i,0):
                for j in range(cols_num):
                    if '/' in str(table.cell_value(i,j)): #判断当前是否是中枢格
                        zhongshu   = str(table.cell_value(i,j))
                        zhongshudi = zhongshu.split('/')[0] #中枢顶
                        zhongshuding = zhongshu.split('/')[1] #中枢底
                        if not 'pending' in str(table.cell_value(i,j+1)): #pending格的计划被跳过
                            if '1' in str(table.cell_value(i,j+1)): #判断当前中枢是否已经有仓位
                                #print(table.cell_value(i,j))
                                if(float(current_stock_price) >= float(zhongshuding)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"], "MSG: 触发1D中枢卖出 @Strategy Monitor", stock_name+", 触发中枢: 1D -> "+zhongshu, "")
                            else:
                                if(float(current_stock_price) <= float(zhongshudi)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"], "MSG: 触发1D中枢买入 @Strategy Monitor", stock_name+", 触发中枢: 1D -> "+zhongshu, "")
            #处理30分钟级别中枢
            if '30F' in table.cell_value(i, 0):
                for j in range(cols_num):
                    if '/' in str(table.cell_value(i, j)):  # 判断当前是否是中枢格
                        zhongshu = str(table.cell_value(i, j))
                        zhongshudi = zhongshu.split('/')[0]  # 中枢顶
                        zhongshuding = zhongshu.split('/')[1]  # 中枢底
                        if not 'pending' in str(table.cell_value(i, j + 1)):  # pending格的计划被跳过
                            if '1' in str(table.cell_value(i, j + 1)):  # 判断当前中枢是否已经有仓位
                                # print(table.cell_value(i,j))
                                if (float(current_stock_price) >= float(zhongshuding)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"], "MSG: 触发30F中枢卖出 @Strategy Monitor",
                                                            stock_name + ", 触发中枢: 30F -> " + zhongshu, "")
                            else:
                                if (float(current_stock_price) <= float(zhongshudi)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"], "MSG: 触发30F中枢买入 @Strategy Monitor",
                                                            stock_name + ", 触发中枢: 30F -> " + zhongshu, "")
if __name__=="__main__":
    xl_analyser0 = excel_analyser()
    my_table=xl_analyser0.zs_wg_analyse(r'C:\Users\hyqin\Desktop\Strategy_Monitor\zhongshu_wangge.xlsx')
