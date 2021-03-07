import requests
import json
import qrcode
import os
import time
import random
import hashlib

pwd = os.path.dirname(os.path.abspath(__file__))

def MakeQrcode(message):
    img = qrcode.make(message)
    ImgPath = os.path.join(pwd, "qrcode.png")
    img.save(ImgPath)
    return ImgPath

def SplitLoginInfo(url):
    keywords = url[len("https://passport.biligame.com/crossDomain?"):][:-len("&gourl=http%3A%2F%2Fwww.bilibili.com")]
    cookies = keywords.replace("&", "; ")
    return cookies

def WebLogin():
    url = "https://passport.bilibili.com/qrcode/getLoginUrl"
    res = json.loads(requests.get(url).text)
    qrocde_url = res["data"]["url"]
    oauthKey = res["data"]["oauthKey"]
    img_path = MakeQrcode(qrocde_url)
    print(f"二维码位于 {img_path}，请手机扫描后确认登录")
    while True:
        time.sleep(1)
        url = "https://passport.bilibili.com/qrcode/getLoginInfo"
        data = {
            "oauthKey": oauthKey,
            "gourl": "http://www.bilibili.com",
        }
        res = json.loads(requests.post(url, data = data).text)
        if res["status"] == True:
            os.remove(img_path)
            return res
            # cookies = SplitLoginInfo(res["data"]["url"])

def GetRandomString(num):
    return ''.join(random.sample("ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789", num))

def CalcSign(data):
    parms = ""
    for value in data:
        parms = parms + str(value) + "=" + str(data[value]) + "&"
    parms = parms[:-1] + "59b43e04ad6965f34319062b478f83dd" # TV段专用盐值，appkey=4409e2ce8ffd12b8，appsec=59b43e04ad6965f34319062b478f83dd
    sign = hashlib.md5(parms.encode("utf-8")).hexdigest()
    data["sign"] = sign
    return data

def TVLogin1():
    url = "http://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code"
    buvid = GetRandomString(37)
    nosign_data = {
        "appkey": "4409e2ce8ffd12b8",
        "local_id": buvid,
        "ts": int(time.time()),
    }
    signed_data = CalcSign(nosign_data)
    res = json.loads(requests.post(url, data=signed_data).text)
    
    qrocde_url = res["data"]["url"]
    auth_code = res["data"]["auth_code"]
    img_path = MakeQrcode(qrocde_url)
    print(f"二维码位于 {img_path}，请手机扫描后确认登录")
    
    while True:
        time.sleep(1)
        url = "https://passport.bilibili.com/x/passport-tv-login/qrcode/poll"
        nosign_data = {
            "appkey": "4409e2ce8ffd12b8",
            "auth_code": auth_code,
            "local_id": buvid,
            "ts": int(time.time()),
        } # 务必保证其键值对的顺序，否则可能会盐值校验错误
        signed_data = CalcSign(nosign_data)
        res = json.loads(requests.post(url, data=signed_data).text)
        if res["code"] == 0:
            os.remove(img_path)
            return res

def TVLogin2():
    url = "https://passport.snm0516.aisee.tv/x/passport-tv-login/qrcode/auth_code"
    deviceId = GetRandomString(20)
    buvid = GetRandomString(37)
    fingerprint = time.strftime("%Y%m%d%H%M%S", time.localtime()) + GetRandomString(45)
    nosign_data = {
        "appkey": "4409e2ce8ffd12b8",
        "auth_code": "",
        "bili_local_id": deviceId,
        "build": "102801",
        "buvid": buvid,
        "channel": "master",
        "device": "OnePlus",
        "device_id": deviceId,
        "device_name": "OnePlus7TPro",
        "device_platform": "Android10OnePlusHD1910",
        "fingerprint": fingerprint,
        "guid": buvid,
        "local_fingerprint": fingerprint,
        "local_id": buvid,
        "mobi_app": "android_tv_yst",
        "networkstate": "wifi",
        "platform": "android",
        "sys_ver": "29",
        "ts": int(time.time()),
    }
    signed_data = CalcSign(nosign_data)
    res = json.loads(requests.post(url, data=signed_data).text)
    
    qrocde_url = res["data"]["url"]
    auth_code = res["data"]["auth_code"]
    img_path = MakeQrcode(qrocde_url)
    print(f"二维码位于 {img_path}，请手机扫描后确认登录")
    
    while True:
        time.sleep(1)
        url = "https://passport.bilibili.com/x/passport-tv-login/qrcode/poll"
        nosign_data["auth_code"] = auth_code
        nosign_data["ts"] = int(time.time())
        nosign_data.pop("sign") # 删除之前计算的sign值（因为共用data的关系）
        signed_data = CalcSign(nosign_data)
        res = json.loads(requests.post(url, data=signed_data).text)
        if res["code"] == 0:
            os.remove(img_path)
            return res

def RefreshLogin(access_token, refresh_token):
    url = "https://passport.bilibili.com/api/v2/oauth2/refresh_token"
    nosign_data = {
        "access_key": access_token,
        "appkey": "4409e2ce8ffd12b8",
        "refresh_token": refresh_token,
        "ts": int(time.time()),
    }
    signed_data = CalcSign(nosign_data)
    res = json.loads(requests.post(url, data = signed_data).text)
    return res


def main():
    a = WebLogin()
    print(a)
    cookies = SplitLoginInfo(a["data"]["url"])
    print(cookies)
    print()
    
    a = TVLogin1()
    print(a)
    access_token = a["data"]["access_token"]
    refresh_token = a["data"]["refresh_token"]
    b = RefreshLogin(access_token, refresh_token)
    print(b)
    print()

    a = TVLogin2()
    print(a)
    access_token = a["data"]["access_token"]
    refresh_token = a["data"]["refresh_token"]
    b = RefreshLogin(access_token, refresh_token)
    print(b)

if __name__ == '__main__':
    main()