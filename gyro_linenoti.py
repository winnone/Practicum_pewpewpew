import usb
import requests

from practicum import find_mcu_boards, McuBoard, PeriBoard
from time import sleep

devs = find_mcu_boards()
url = 'https://notify-api.line.me/api/notify'
token = 'uplxOg1ZodT1lWdJ1FvRSgoJCSIgrff8FZ03r9skusQ'
headers = {
            'content-type':
            'application/x-www-form-urlencoded',
            'Authorization':'Bearer '+token
           }

if len(devs) == 0:
    print("*** No practicum board found.")
    exit(1)

mcu = McuBoard(devs[0])
print("*** Practicum board found")
peri = PeriBoard(mcu)

while True:
    try:
        gr = peri.get_gyro()

        if gr is True:
            state = "Normal"
        else:
            state = "Fall"
            r = requests.post(url, headers=headers , data = {'message':'ตรวจพบการล้ม'})
            while gr is False:
                gr = peri.get_gyro()

        print("gyro state: %-8s" % (state))
        sleep(0.5)

    except usb.core.USBError:
        print("USB error detected")