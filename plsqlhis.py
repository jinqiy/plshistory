#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import struct
import datetime
import csv

def day2date(day):
  d = datetime.date(1899,12,30)
  return (d + datetime.timedelta(day)).isoformat()

def time2timestr(time):
  dall = 24 * 60 * 60
  hour_l = dall * time / 60 / 60
  hour = int(hour_l)
  minute_l = (hour_l - hour) * 60
  minute = int(minute_l)
  second_l = (minute_l - minute) * 60
  second = int(second_l)
  return str(hour) + ':' + str(minute) + ':' + str(second)

def write2file(fname,lines):
  with open(fname,'w') as csvfile: 
    writer = csv.writer(csvfile,quoting=csv.QUOTE_ALL)
    #先写入columns_name
    writer.writerow(['sequence','datetime','user','database','text'])
    writer.writerows(lines)  
 
def readPLSRecall(fname):
  histline=[]
  f=open(fname,'rb')
  size = os.path.getsize(fname)
  for i in range(0, size,4125):
    data=f.read(4)
    seq = struct.unpack("I", data)[0]
    data=f.read(8)
    #data_float = struct.unpack("f", data)[0]
    data_double = struct.unpack("d", data)[0]
    day_int = int(data_double)
    time_long = data_double - int(data_double)
    data = f.read(31)
    username = bytes.decode(data).rstrip('\x00')
    data = f.read(81) 
    database = bytes.decode(data).rstrip('\x00')
    data = f.read(4001)
    try:
    #text = str(data, encoding = "gbk").rstrip('\x00')
      text = str(data.rstrip(b'\x00').replace(b'\x00',b''),encoding="gbk")
    except:
      print(data)
    histline.append([str(seq),day2date(day_int) +' '+ time2timestr(time_long),username,database,text])
    print(histline)
  f.close()
  return histline

if __name__ == "__main__":
  fname = './PLSRecall.dat'
  histline = readPLSRecall(fname)
  csvfname = './PLShist.csv'
  write2file(csvfname,histline)

