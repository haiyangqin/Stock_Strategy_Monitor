#!/usr/bin/python

#encoding=utf-8
import xlrd
import pandas as pd
import Stock_Monitor
import Files_EmailSender
import Draw_Picture
import datetime

class excel_analyser(object):

    def csv2xl(self,csv_name):
        '''
        csv转xl
        '''
        csv=pd.read_csv(csv_name,encoding='utf-8')
        csv.to_excel(r'zhongshu_wangge.xlsx', sheet_name='tmp_data')

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
                #print(geted_info.describe) #DBG --> stock info
                geted_stock_name = geted_info.describe.split('股票名称：')[1].split('，')[0].replace(' ','')
                if(geted_stock_name != stock_name):
                   print('股票名称和代码不对应，请检查excel表格！')
                   print('geted_stock_name:'+geted_stock_name+' '+'expected_stock_name:'+stock_name)
                   err_senders0 = Files_EmailSender.Carry_files_EmailSender()
                   err_senders0.send_email(["420195048@qq.com"],
                                           "ERR: 股票名称和代码不对应 @Strategy Monitor",
                                           "股票名称和代码不对应: "+stock_name+""+stock_id+" -> "+"实获名称："+geted_stock_name,"")
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
                                    msg_senders0.send_email(["420195048@qq.com"],
                                                            "MSG: 触发1D中枢卖出 @Strategy Monitor",
                                                            stock_name+", 触发中枢: 1D -> "+zhongshu, "")
                            else:
                                if(float(current_stock_price) <= float(zhongshudi)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"],
                                                            "MSG: 触发1D中枢买入 @Strategy Monitor",
                                                            stock_name+", 触发中枢: 1D -> "+zhongshu, "")
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
                                    msg_senders0.send_email(["420195048@qq.com"],
                                                            "MSG: 触发30F中枢卖出 @Strategy Monitor",
                                                            stock_name + ", 触发中枢: 30F -> " + zhongshu, "")
                            else:
                                if (float(current_stock_price) <= float(zhongshudi)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"],
                                                            "MSG: 触发30F中枢买入 @Strategy Monitor",
                                                            stock_name + ", 触发中枢: 30F -> " + zhongshu, "")
            # 处理5分钟级别中枢
            if '5F' in table.cell_value(i, 0):
                for j in range(cols_num):
                    if '/' in str(table.cell_value(i, j)):  # 判断当前是否是中枢格
                        zhongshu = str(table.cell_value(i, j))
                        zhongshudi = zhongshu.split('/')[0]  # 中枢顶
                        zhongshuding = zhongshu.split('/')[1]  # 中枢底
                        if not 'pending' in str(table.cell_value(i, j + 1)):  # pending格的计划被跳过
                            if '1' in str(table.cell_value(i, j + 1)):  # 判断当前中枢是否已经有仓位
                                # print(table.cell_value(i,j))
                                if (float(current_stock_price) >= float(zhongshuding)):
                                    #print('DBG --> 5F, current_stock_price:'+current_stock_price+' '+'zhongshuding:'+zhongshuding)
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"],
                                                            "MSG: 触发5F中枢卖出 @Strategy Monitor",
                                                            stock_name + ", 触发中枢: 5F -> " + zhongshu,
                                                            "")
                            else:
                                if (float(current_stock_price) <= float(zhongshudi)):
                                    msg_senders0 = Files_EmailSender.Carry_files_EmailSender()
                                    msg_senders0.send_email(["420195048@qq.com"],
                                                            "MSG: 触发5F中枢买入 @Strategy Monitor",
                                                            stock_name + ", 触发中枢: 5F -> " + zhongshu,
                                                            "")

    def zs_wg_analyse_positions(self, xl_name):
        '''
        中枢 网格 表
        xl_name: 表格名称
        '''
        xl_opened = xlrd.open_workbook(xl_name)
        table = xl_opened.sheets()[0]
        rows_num = table.nrows
        cols_num = table.ncols
        # print(rows_num)
        # print(cols_num)
        current_positions = []
        holding = 0
        for i in range(rows_num):
            # print(table.cell_value(i,0))
            if '交易品种' in table.cell_value(i, 0):
                content = table.cell_value(i, 1)
                stock_name = content.split('（')[0]  # 股票名称
                stock_id = content.split('（')[1].split('）')[0]  # 股票代码
                temp = Stock_Monitor.Share(stock_id, 0, 0)
                geted_info = Stock_Monitor.getrealtimedata(temp)
                # print(geted_info.describe) #DBG --> stock info
                geted_stock_name = geted_info.describe.split('股票名称：')[1].split('，')[
                    0].replace(' ', '')
                if (geted_stock_name != stock_name):
                    print('股票名称和代码不对应，请检查excel表格！')
                    print(
                        'geted_stock_name:' + geted_stock_name + ' ' + 'expected_stock_name:' + stock_name)
                    err_senders0 = Files_EmailSender.Carry_files_EmailSender()
                    err_senders0.send_email(["420195048@qq.com"],
                                            "ERR: 股票名称和代码不对应 @Strategy Monitor",
                                            "股票名称和代码不对应: " + stock_name + "" + stock_id + " -> " + "实获名称：" + geted_stock_name,
                                            "")
                current_stock_price = geted_info.price
            # 处理日线级别中枢
            if '1D' in table.cell_value(i, 0):
                for j in range(cols_num):
                    if '/' in str(table.cell_value(i, j)):  # 判断当前是否是中枢格
                        zhongshu = str(table.cell_value(i, j))
                        zhongshudi = zhongshu.split('/')[0]  # 中枢顶
                        zhongshuding = zhongshu.split('/')[1]  # 中枢底
                        if not 'pending' in str(
                                table.cell_value(i, j + 1)):  # pending格的计划被跳过
                            if '1' in str(table.cell_value(i, j + 1)):  # 判断当前中枢是否已经有仓位
                                # print(table.cell_value(i,j))
                                # print(stock_name)
                                holding = holding + 1
            if (holding != 0):  # record holding item and positons
                current_positions.append((stock_name, holding))
            holding = 0
        positions_drawer0 = Draw_Picture.Picture_Drawer()
        print(current_positions)
        positions_drawer0.draw_rose_piture(current_positions)

    def yield_analyse(self, xl_name):
        '''
        中枢 网格 表
        xl_name: 表格名称
        '''
        xl_opened = xlrd.open_workbook(xl_name)
        table = xl_opened.sheets()[0]
        rows_num = table.nrows
        cols_num = table.ncols
        # print(rows_num)
        # print(cols_num)
        my_date = []
        my_ratio = []
        for i in range(1,rows_num): #row 1 is the title
             date = xlrd.xldate_as_tuple(table.cell_value(i,0),0)
             current_date = str(date[1])+'-'+str(date[2])
             current_ratio = table.cell_value(i,2) * 100
             if(current_date != ''):
               my_date.append(current_date)
             if(current_ratio != ''):
               my_ratio.append(current_ratio)
        print(my_date,my_ratio)
        return my_date,my_ratio




if __name__=="__main__":
    xl_analyser0 = excel_analyser()
    #my_table=xl_analyser0.zs_wg_analyse(r'C:\Users\hyqin\Desktop\my_test\zhongshu_wangge.xlsx')
    my_positions=xl_analyser0.zs_wg_analyse_positions(r'.\zhongshu_wangge.xlsx')
    #my_positions=xl_analyser0.yield_analyse(r'.\yield.xlsx')
