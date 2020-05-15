#!/usr/bin/python

#encoding=utf-8

import schedule
import time
import threading
import Excel_Analyser

def job0(): #个股操作中枢观测
    print("job0 is running !!!")
    now_time = time.localtime()
    my_time = (now_time.tm_hour)*100 + now_time.tm_min
    #print(my_time)
    if ((my_time >= 925) and (my_time < 1130 )) or ((my_time >= 1257) and (my_time < 1500 )):
        xl_analyser0 = Excel_Analyser.excel_analyser()
        my_table = xl_analyser0.zs_wg_analyse(r'.\zhongshu_wangge.xlsx')



def job2():
    print("I'm working... in job2")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(15).seconds.do(run_threaded, job0)
#schedule.every(10).seconds.do(run_threaded, job)
#schedule.every(10).seconds.do(run_threaded, job2)

while True:
    schedule.run_pending()
    time.sleep(1)
