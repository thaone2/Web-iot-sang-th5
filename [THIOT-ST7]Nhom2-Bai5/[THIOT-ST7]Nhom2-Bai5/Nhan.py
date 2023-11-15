from urllib import request, parse
import json
from gpiozero import LED 
from datetime import datetime

from time import sleep
import time
led = LED(16) #khai bao chan noi led
def thingspeak_get(): #lay gia tri auto/manual cung gia tri led tu thingspeak iot xuong
    api_key_read = "P8EKRE7448UGLH7T"
    channel_ID = "1723177"
    
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/1/last.json?api_key=%s" %(channel_ID,api_key_read) , method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data["field1"] #gan gia tri value laf gia tri led 1/2
    
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/2/last.json?api_key=%s" %(channel_ID,api_key_read) , method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value1 = respone_data["field2"] #gan gia tri value1 la gia tri cuar mode vs 2 trang thai la auto/manual    
    return value,value1
    
#Auto 1 Manual 2
while True: #tao vong lap while True
        # du lieu duoc gui len kenh 1, du lieu doc xuong tu kenh 2    
        value,value1 = thingspeak_get() #Doc du lieu, value là on/off - value1 là auto/manual
        print('Led: {} , Mode: {} '.format(value, value1))    
        mytime = int(datetime.now().strftime('%H'))  # lay gia tri thoi gian cua raspberry      
        t = int(mytime) 
        print('Time: {}'.format(mytime))
        if value1 == "2":  # xét điều kiện để điều khiển led "2" là off hoặc manual, "1" là on hoặc auto tương ứng.
            if value == "2":
                led.off()
            if value == "1":
                led.on()
        if value1 == "1":
            if t >=3 and t<4:
                led.on()
            else:
                led.off()        
        time.sleep(20)
