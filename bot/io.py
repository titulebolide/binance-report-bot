import requests
import conf
import os

def send_report(msg):
    try:
        requests.post("http://127.0.0.1:"+str(conf.PUBLISH_PORT), data={"txt":msg})
    except requests.exceptions.ConnectionError:
        print(msg)

def send_img(img):
    try:
        requests.post("http://127.0.0.1:"+str(conf.PUBLISH_PORT), data={
            "img": os.path.join(os.getcwd(), img)
        })
    except requests.exceptions.ConnectionError:
        pass
