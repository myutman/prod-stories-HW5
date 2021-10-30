import requests
import base64
import json
from time import sleep

API_HOST = "http://45.14.48.80:10000"


def get_results():
    r = requests.get(API_HOST + "/results")
    return r.text


def upload_file(filename):
    r = requests.post(
        API_HOST + "/upload", 
        files={"file": open(filename, "rb")},
        headers={"User-Id": "myutman"}
    )
    info = json.loads(r.text)
    return info


def run_task(info):
    info = info.copy()
    info["version"] = "1"
    info["is_part"] = False
    info['file'] = info['filename']
    info.pop('filename')
    
    r = requests.post(API_HOST + "/task", json.dumps(info))
    while r.status_code == 409:
        sleep(0.01)
        r = requests.post(API_HOST + "/task", json.dumps(info))
    
    return r.status_code == 202, r.reason


def wait_for_task():
    r = requests.get(API_HOST + "/healthcheck")
    data = json.loads(r.text)
    while data["status"] != "COMPLETED":
        sleep(0.01)
        r = requests.get(API_HOST + "/healthcheck")
        data = json.loads(r.text)


def kill_task():
    r = requests.post(
        API_HOST + "/stop"
    )