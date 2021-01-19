import re
import requests

ipcode=''
cookie=[]
ipcode_regx='<input type="hidden" name="ipcode" id="ipcode" value="(.*?)" />'
acct_regx='"(.*?)"'
def getipcode():
    url = 'http://ha.189.cn/kd/'
    headers = {
        "Host": "ha.189.cn",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 Safari/537.36 Edg/88.0.705.22",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }
    response = requests.get(url=url, headers=headers)
    cookie.append(response.cookies["JSESSIONID"])
    cookie.append(response.cookies["wt_fore_vs"])
    if response.status_code == 200:
        global ipcode
        ipcode=re.findall(ipcode_regx,response.text)[0]
        print(ipcode)
        return
    else:
        print(response.status_code)
        return response.status_code

def getAcct():
    url = 'http://ha.189.cn/dwr/call/plaincall/Service.excute.dwr'
    headers = {
        "Host": "ha.189.cn",
        "Connection": "keep-alive",
        "Content-Length": "411",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 Safari/537.36 Edg/88.0.705.22",
        "Content-Type": "text/plain",
        "Accept": "*/*",
        "Origin": "http://ha.189.cn",
        "Referer": "http://ha.189.cn/kd/",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": "JSESSIONID=" + cookie[0] + "; wt_fore_vs=" + cookie[1],
    }
    payloadData = {
        'callCount': 1,
        'page': '/kd/',
        'httpSessionId': '',
        'scriptSessionId': 'AA0CBE9FB90164F9E0E55CF74FCC9338544',
        'c0-scriptName': 'Service',
        'c0-methodName': 'excute',
        'c0-id': '0',
        'c0-param0': 'string:KDTS_TEST',
        'c0-param1': 'boolean:false',
        'c0-e1': 'string:',
        'c0-e2': 'string:' + ipcode,
        'c0-e3': 'number:182',
        'c0-e4': 'string:sxkdTest',
        'c0-param2': 'Object_Object:{telephone:reference:c0-e1, ipcode:reference:c0-e2, rule:reference:c0-e3, method:reference:c0-e4}',
        'batchId': '0',
    }
    try:
        response=requests.post(url=url, headers=headers,data=payloadData)
        if response.status_code == 200:
            acct = re.findall(acct_regx, response.text.encode('utf-8').decode('unicode_escape'))[3]
            print(acct)
            return acct
        else:
            print(response.status_code)
            return response.status_code
    except requests.ConnectionError as e:
        print('Error', e.args)
    return

def ts():
    getipcode()
    acct=getAcct()
    url = 'http://ha.189.cn/dwr/call/plaincall/Service.excute.dwr'
    headers = {
        "Host": "ha.189.cn",
        "Connection": "keep-alive",
        "Content-Length": "426",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 Safari/537.36 Edg/88.0.705.22",
        "Content-Type": "text/plain",
        "Accept": "*/*",
        "Origin": "http://ha.189.cn",
        "Referer": "http://ha.189.cn/kd/",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": "JSESSIONID=" + cookie[0] + "; wt_fore_vs=" + cookie[1],
    }
    payloadData = {
        'callCount': 1,
        'page': '/kd/',
        'httpSessionId': '',
        'scriptSessionId': 'AA0CBE9FB90164F9E0E55CF74FCC9338544',
        'c0-scriptName': 'Service',
        'c0-methodName': 'excute',
        'c0-id': '0',
        'c0-param0': 'string:KDTS_TEST',
        'c0-param1': 'boolean:false',
        'c0-e1': 'string:' + acct,
        'c0-e2': 'string:' + ipcode,
        'c0-e3': 'number:182',
        'c0-e4': 'string:kdts',
        'c0-param2': 'Object_Object:{dial_acct:reference:c0-e1, ipaddr:reference:c0-e2, rule:reference:c0-e3, method:reference:c0-e4}',
        'batchId': '1',
    }
    try:
        response=requests.post(url=url, headers=headers,data=payloadData)
        if response.status_code == 200:
            print(response.text.encode('utf-8').decode('unicode_escape'))
            return response.text
        else:
            print(response.status_code)
            return response.status_code
    except requests.ConnectionError as e:
        print('Error', e.args)
    return

if __name__ == '__main__':
    ts()
