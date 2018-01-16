# -*- coding:utf-8 -*-
# Write By Sunwl
# 2017/10/19
#
# 爬取猫眼 TOP100 热门电影
#
# python 3.6.2
# 运行环境 Win，Linux
# 注意：

from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re
import json

#　获取一个url网页的逻辑
def get_one_page(url):
    # 设置 headers 模拟浏览器
    headers = {
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With" : "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
    }
    try:
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        if response.status_code == 200: # status ok
            return response.text
        return None
    except RequestException:
        return None

#　提取一个url网页信息的逻辑
def deal_real_page(html):
    # 筛选 匹配项
    pattern = re.compile('<p class="name">.*?title="([\s\S]*?)"[\s\S]*?data-act=[\s\S]*?<p class="star">([\s\S]*?)</p>[\s\S]*?<p class="releasetime">([\s\S]*?)</p>    </div>') #???
    results = re.findall(pattern, html)
    for item in results:
        yield{
           'title': item[0],
           'star': item[1],
           'releasetime': item[2]
        }

# 存取一个url中要保存的信息的逻辑
def write_file(content):
    with open("maoyan.txt", 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

# 构造一个起始的url链接
def get_top(offset):
    # 对 url 进行拼接，做到抓取其他页面
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    for item in deal_real_page(html):
        write_file(item)

if __name__ == '__main__':
    # 使用了进程池, 事实上线程也有池
    pool = Pool()
    pool.map(get_top, [i*10 for i in range(10)])
    pool.close()
    pool.join()
    print("over")

    # get_one_page("http://maoyan.com/board/4?offset=0")
