import requests
import time
import _thread

url = "http://www.jctip.com/"

# threadPool = [1]*100

def print_time( threadName, delay):
    count = 0
    while 1:
        requests.get(url)
        if threadName == "Thread-1":
            count += 1
            print(threadName, count,"do request")

try:
    for index in range(100):
        _thread.start_new_thread( print_time, ("Thread-"+ str(index), 2, ) )

except:
    print("Error: unable to start thread") 

while 1:
    time.sleep(1)
    pass