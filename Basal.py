import time
import glob
import re
import MySQLdb
import time
import datetime


sensorPaths = [path+"/w1_slave" for path in glob.glob("/sys/bus/w1/devices/28*")]
re_temp = re.compile("t=(\d+)")

conn = MySQLdb.connect(host= "localhost", user="root",
              passwd="Wanze", db="BasalDB")
x = conn.cursor()


def convTemp(tempStr):
    try:
        temp = int(re_temp.search(s).group(1))
        temp /= 1000
        return temp
    except:
        return 999.999


with open(sensorPaths[0], "r") as ts1,\
     open(sensorPaths[1], "r") as ts2:

    while True:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        temp1 = convTemp(ts1.read())
        temp2 = convTemp(ts2.read())

        try:
            x.execute("INSERT into basal (date, temp1, temp2) values({},{},{})".format(timestamp,temp1,temp2))
            conn.commit()
        except:
            conn.rollback()

conn.close()
