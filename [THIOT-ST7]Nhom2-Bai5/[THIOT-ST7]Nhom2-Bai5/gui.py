from urllib import request, parse #khai bao thu vien ho tro de gui du lieu len server theo giao thuc http
from time import sleep #Khai bao sleep tu thu vien time
from seeed_dht import DHT #khai bao thu ven cho cam bien
sensor = DHT('11',5) #ket noi chan cam bien 
def make_param_thingspeak(humi, temp): #chuogn trinh con tao chuoi du lieu len server
    params = parse.urlencode({'field1': humi, 'field2': temp}).encode() #ma hoa va dinh dang cac thong so se gui len server
    return params #tra ve gia tri params

def thingspeak_post(params): #chuong trinh con gui chuoi du lieu len server theo http
    api_key_write = "JSMIKVY0LHBR4SBI" #khoa api ghi du lieu
    req = request.Request('https://api.thingspeak.com/update', method="POST") #gui yeu cau len server thong bao se gui du lieu len
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    r = request.urlopen(req, data = params) #ma hoa cac thong so
    respone_data = r.read() #dox cac gia tri gui len data va gan vao ien response_data

while True:
    try: #
        humi, temp = sensor.read() #doc nhit do, do am do duoc tu cam bien
        params_thingspeak = make_param_thingspeak(humi,temp) #tao chuoi du lieu de gui len server
        data = thingspeak_post(params_thingspeak) #gui chuoi du lieu len server
        print("Do am: ",humi,' ',"Nhiet do: ",temp) #In ra man hinh console gia tri nhiet do, do am, random
        sleep(20) #delay 20s cho moi lan gui
    except: #truong hop ngoai le
        print("khong co ket noi mang")  #bao mat ket noi mang
        sleep(2)
