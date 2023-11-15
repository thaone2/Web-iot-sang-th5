from urllib import request, parse
from time import sleep
import time
from seeed_dht import DHT
from gpiozero import LED
import json
from datetime import datetime
from datetime import timedelta

sensor = DHT('11',5) 
led = LED(16)

def thingspeak_post(Temp,Hum):
    params = parse.urlencode({'field1': Temp,'field2': Hum}).encode()
    API_Key_Write= "CVW77OQ3699SDMD1"
    req = request.Request('https://api.thingspeak.com/update',method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY",API_Key_Write)
    r = request.urlopen(req,data = params)
    respone_data=r.read()
    return respone_data

def thingspeak_get():
    api_key_read = "SQC01J6OU6LS25MX"
    channel_ID = "2338557"
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/1/last.json?api_key=%s" %(channel_ID,api_key_read) , method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data["field1"]
    
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/2/last.json?api_key=%s" %(channel_ID,api_key_read) , method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value1 = respone_data["field2"]
    return value,value1
    
while True: 
        doam, nhietdo = sensor.read()
        thingspeak_post(nhietdo,doam)
        value,value1 = thingspeak_get() #Doc du lieu, value là on/off - value1 là auto/manual
        print('on/off {} , auto/manual {} '.format(value, value1))
        print('Nhiet do {}C, Do am {}%'.format(nhietdo, doam))  # in ra man hinh
        mytime = int(datetime.now().strftime('%H'))  # lay gia tri thoi gian cua raspberry
        mytime1 = int(datetime.now().strftime('%M'))
        mytime2 = int(datetime.now().strftime('%S'))
        mytime3 = timedelta(hours = mytime, minutes = mytime1, seconds = mytime2)
        # timedelta chỉ ngày , giây và micro giây được lưu trữ bên trong và chuyển đổi :
        # mili giây sang 1000 micro giây,
        # Một phút được chuyển đổi thành 60 giây.
        # Một giờ được chuyển đổi thành 3600 giây.
        # Một tuần được chuyển đổi thành 7 ngày.
        t = int(mytime3.total_seconds()) # tính tổng số giây để so sánh
        print(t)
        print('{} : {} : {}'.format(mytime,mytime1,mytime2))
        if value1 == "2":  # xét điều kiện để điều khiển led "2" là off hoặc manual, "1" là on hoặc auto tương ứng.
            if value == "2":
                led.off()
            if value == "1":
                led.on()
        if value1 == "1":
            if t > 36000 and t < 37200: #36000s là 10h , 37200s là 10h20'
                led.on()
            else:
                led.off()
        time.sleep(20)