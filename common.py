# -*- coding: utf-8 -*-
#!/usr/bin/python3
import socks
import urllib.request as urllib2
import requests
from sockshandler import SocksiPyHandler
import config as config
from bson.objectid import ObjectId
import random
import string
import time
import hashlib


# 检查必须字段
def checkRequire(data, fields):
    # 多维数组
    if isinstance(data, list):
        for childData in data:
            return checkRequire(childData, fields)
    else:
        # 从必须字段中 找不存在于 data 中的 key
        for k in fields:
            if k not in data:
                return k
    return True

# 移除非法字段  转换字段类型
'''
fields 合法字段 list
convertFields 转换字段类型 dict
'''
def removeUnsafeFields(data, fields, convertFields):
    # 多维数组
    if isinstance(data, list):
        safeData = []
        for childData in data:
            safeData.append(removeUnsafeFields(childData, fields, convertFields))
    else:
        safeData = {}
        for k, v in data.items():
            if k not in fields:
                continue
            safeData[k] = conv2(v, convertFields[k])
    return safeData


# 转换类型
def conv2(v, stype):
    if 'objectid' == stype:
        return ObjectId(v)
    if 'string' == stype:
        return str(v)
    if 'int' == stype:
        return int(v)
    if 'dict' == stype:
        return dict(v)
    if 'list' == stype:
        return list(v)
    if 'bool' == stype:
        return bool(v)
    # 原始类型
    return v

# 中文化显示 播放量数量
def getPlayNumTxt(playnum):
    try:
        playnum = int(playnum)
        if playnum < 10000:
            return str(playnum) 
        if playnum >= 10000 and playnum < 100000000:
            return str(round(playnum / 10000, 1)) + '万'
        if playnum >= 100000000:
            return str(round(playnum / 100000000, 1)) + '亿'
    except ValueError as msg:
        return playnum

# 中文转数字化
def getRealPlayNum(numtxt):
    if -1 != numtxt.find('亿'):
        num = numtxt.replace('亿', '').strip()
        return int(float(num) * 100000000)
    if -1 != numtxt.find('万'):
        num = numtxt.replace('万', '').strip()
        return int(float(num) * 10000)
    if -1 != numtxt.find('千'):
        num = numtxt.replace('千', '').strip()
        return int(float(num) * 1000)

# 获取随机名称 目录名/文件夹
def genRandName(length = 5):
    return ''.join(random.sample(string.digits+string.ascii_letters * 10, length))

# 是否该休息了
def canISleep():
    print('任务开始 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    # 23 - 2点休息
    nhour = int(time.localtime(time.time()).tm_hour)
    if (nhour >= 23 or nhour <= 6):
        print('Sleep time, quit!') 
        exit()
    return True

# 对文件做 md5 验证完整性
def fileHashMd5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 显示错误信息
def ex(msg, info = None):
    print(msg)
    if info:
        print(info)
    return False