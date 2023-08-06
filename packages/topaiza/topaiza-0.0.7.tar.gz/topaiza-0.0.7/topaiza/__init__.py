import sys
import pprint as pp
import requests
import json

def get(url):
    r = requests.get(url)
    if r:
        if(r.headers.get('content-type') == 'application/json'):
            parsedJson = r.text
            parsedJson = parsedJson.json
            return parsedJson
        else:
            return r.text

def post(url, data):
    r = requests.post(url, data=data)
    if r:
        if(r.headers.get('content-type') == 'application/json'):
            handleJson(r.text)
        else:
            handleResp(r.text)

def massGet(urls):
    for url in urls:
        r = requests.get(url)
        if r:
            if(r.headers.get('content-type') == 'application/json'):
                handleJson(r.text)
            else:
                handleResp(r.text)

def massPost(urls, datas):
    for url in urls:
        for data in datas:
            r = requests.post(url, data=data)
            if r:
                if(r.headers.get('content-type') == 'application/json'):
                    handleJson(r.text)
                else:
                    handleResp(r.text)



def handleJson(jsonResp):
    parsedResponse = jsonResp.json()
    return parsedResponse

def handleResp(normalResp):
    return normalResp