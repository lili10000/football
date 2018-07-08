import requests
import time

rate = 0.03

date = time.strftime("%Y-%m-%d",time.localtime())

url = "http://www.365rich.com/handle/football/1x2.aspx?companyid=0&date="+date
# print(url)
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
    if (start_rate - end_rate) >= rate:
        print(id[4:], round(abs(start_rate - end_rate),2), "主队升水， 客队降水")
    elif (end_rate - start_rate) > rate:
        print(id[4:], round(abs(start_rate - end_rate),2), "主队降水， 客队升水")
    # else:
    #     print(id[4:], round(start_rate,2), round(end_rate,2), round(abs(start_rate - end_rate),2))
    
    


    end_pos += 4
    s = s[end_pos:]