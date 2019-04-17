import time
from datetime import datetime, timedelta
import data_v8 as updata
import data_v7 as lostCheck
import data_v4 as winCheck
import data_v9 as rateWinCheck
import data_v10 as rateDivCheck
import _thread

SECONDS_PER_DAY = 24 * 60 * 60
 
def getSleepTime():
    
    # curTime = datetime.now()
    # desTime = curTime.replace(hour=6, minute=0, second=0, microsecond=0)
    # delta = curTime - desTime
    # skipSeconds = SECONDS_PER_DAY - delta.total_seconds()
    # print ("Must sleep %d seconds" % skipSeconds)
    # return skipSeconds
    return 5*60


def doOnePerDay():
    while 1:
        time.sleep(6*60*60)
        updata.doUpdata()

_thread.start_new_thread(doOnePerDay, ())
        
while 1:
    start = int(time.time()) 
    print ("start work", datetime.now())
    # updata.doUpdata()
    
    # winCheck.doDayWork()
    rateWinCheck.doDayWork()
    # rateBigCheck.doDayWork()
    rateDivCheck.doDayWork()
    
    end = int(time.time()) 
    print ("end work", end,"    use time=",end-start," s" )
    sleepTime = getSleepTime()
    time.sleep(sleepTime)

    

    