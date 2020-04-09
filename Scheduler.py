#!/usr/bin/python

#encoding=utf-8

import schedule
import time
import threading
import Excel_Analyser

def job0(): #个股操作中枢观测
    print("job0 is running !!!")
    xl_analyser0 = Excel_Analyser.excel_analyser()
    my_table = xl_analyser0.zs_wg_analyse(r'C:\Users\hyqin\Desktop\Strategy_Monitor\zhongshu_wangge.xlsx')



def job2():
    print("I'm working... in job2")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(10).seconds.do(run_threaded, job0)
#schedule.every(10).seconds.do(run_threaded, job)
#schedule.every(10).seconds.do(run_threaded, job2)

while True:
    schedule.run_pending()
    time.sleep(1)
