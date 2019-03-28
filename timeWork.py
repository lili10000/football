import time
from datetime import datetime, timedelta
import data_v8 as updata
import data_v7 as lostCheck
import data_v4 as winCheck
import _thread

SECONDS_PER_DAY = 24 * 60 * 60
 
def getSleepTime():
    
    curTime = datetime.now()
    desTime = curTime.replace(hour=12, minute=0, second=0, microsecond=0)
    delta = curTime - desTime
    skipSeconds = SECONDS_PER_DAY - delta.total_seconds()
    print ("Must sleep %d seconds" % skipSeconds)
    return skipSeconds


        
while 1:

    start = int(time.time()) 
    print ("start work", datetime.now())
    updata.doUpdata()
    _thread.start_new_thread(lostCheck.doDayWork)
    winCheck.doDayWork()

    end = int(time.time()) 
    print ("end work", end,"    use time=",end-start," s" )
    sleepTime = getSleepTime()
    time.sleep(sleepTime)

    

    