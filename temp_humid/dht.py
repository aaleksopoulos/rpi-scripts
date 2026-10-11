# pip install adafruit-circuitpython-dht
# python -m venv venv
# source venv/bin/activate
#*/5 * * * * /home/atalex/dht/venv/bin/python /home/atalex/dht/dht.py -r kid_office 2>> cronerror.log

import board, adafruit_dht, csv, time, argparse, os, sys, requests
from dotenv import load_dotenv, dotenv_values
load_dotenv()

parser = argparse.ArgumentParser(description="Choose the name of the room that you want to measure humidity and temerature")
parser.add_argument('-r', '--room', help="the name of the room", default="default_room", type=str)
args = parser.parse_args()
#print(args.room)

#DHT_PIN = 17 #GPIO pin
#DHT_DEVICE = Adafruit_DHT.DHT22
DHT_DEVICE = adafruit_dht.DHT22(board.D17)

out_file = open('{}.csv'.format(args.room), 'a')
writer = csv.writer(out_file)
i = 0

FLASK_SERVER_URL = "".join(["http://",os.getenv("WEBSERVER_IP"),":",os.getenv("PORT"),"/api/update"])
print(FLASK_SERVER_URL)

while i<10: #try 10 times to read from sensor
    try:
#        humid, temp = Adafruit_DHT.read_retry(DHT_DEVICE, DHT_PIN)
        temp = DHT_DEVICE.temperature
        humid = DHT_DEVICE.humidity
        ctime = time.strftime("%Y-%m-%d %H:%M")

        print("temp : {:04.1f} C".format(temp))
        print("current time : ",ctime)
        print("humid : {:02.0f} %".format(humid))
        writer.writerow([ctime, round(temp, 2),round(humid, 1)])
        out_file.close()

        break
    except Exception as e:
        i+=1
        if i==10:
            with open("dht_error_{}.csv".format(args.room), 'a') as error_file:
                ctime = time.strftime("%Y-%m-%d %H:%M")
                error_file.write("timestamp:{} - there was an error: {}, could not read from sensor for 10 times\n".format(ctime, e))
        time.sleep(1) #wait for 1 sec

if i==10: #all reads failed, nothing to send
    DHT_DEVICE.exit()
    sys.exit(1)

payload = {
    "temperature": temp,
    "humidity": humid,
    "timestamp": ctime
}
try:
    response = requests.post(FLASK_SERVER_URL, json=payload, timeout=10)
    if response.status_code == 200:
        print("payload sent succesfully", response.json())
    else:
        print("problem with payload", response.status_code)
except requests.exceptions.ConnectionError:
    print("could not connect with flask server")
except requests.exceptions.RequestException as e: #timeouts, bad json reply, etc.
    print("problem sending payload:", e)


DHT_DEVICE.exit()
