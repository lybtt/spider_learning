#coding:utf-8
#author：lyb
#Date: 2018/7/28 21:35
import pymongo

import requests
from requests.exceptions import RequestException
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from maoyan_top100.config import *


headers = {"User-Agent": USER_AGENT}


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_one_page(url, headers):
    try:
        global PROXY
        PROXY = get_proxy()
        proxies = {
            'http': 'http://' + PROXY
        }
        if PROXY:
            res = requests.get(url, headers=headers, proxies=proxies)
            if res.status_code == 200:
                return res.text
            return None
        else:
            return get_one_page(url, headers)
    except RequestException:
        return get_one_page(url, headers)


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>'
                         '.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def save_to_mongo(content):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    db[MONGO_TABLE].update({'title': content['title']}, {'$set': content}, True)
    print('存储成功 ：{}'.format(content['title']))


def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url, headers)
    for item in parse_one_page(html):
        # write_to_file(item)
        save_to_mongo(item)

if __name__ == "__main__":
    # 多线程
    start_time = time.time()
    with ThreadPoolExecutor(5) as executor:
        all_task = [executor.submit(main, (num * 10)) for num in range(10)]
        for future in as_completed(all_task):
            data = future.result()
    print('done, takes {} s'.format(time.time() - start_time))
    """
    # 多进程
    start_time = time.time()
    with ProcessPoolExecutor(8) as executor:
        all_task = [executor.submit(main, (num * 10)) for num in range(10)]
        for future in as_completed(all_task):
            data = future.result()
    # for i in range(10):
    #     main(i*10)
    print('done, takes {} s'.format(time.time() - start_time))
    """
