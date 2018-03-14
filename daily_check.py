import requests
import time

rate = 0.04

date = time.strftime("%Y-%m-%d",time.localtime())

url = "http://www.365rich.com/handle/football/1x2.aspx?companyid=0&date="+date
req = requests.get(url)
s = req.text
while not(s.find('i') == -1):
    start_pos = s.find('<i>')
    end_pos = s.find('</i>')
    start_pos +=3
    data = s[start_pos:end_pos]
    dataList = data.split(',')

    id = dataList[1]
    start_win_rate = float(dataList[3])
    # start_ping_rate = dataList[4]
    # start_lost_rate = dataList[5]

    end_win_rate = float(dataList[6])
    # end_ping_rate = dataList[7]
    # end_lost_rate = dataList[8]

    start_rate = 1/start_win_rate
    end_rate = 1/end_win_rate
    if abs(start_rate - end_rate) > rate:
        print(id[4:])
    


    end_pos += 4
    s = s[end_pos:]