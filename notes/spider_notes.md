# urllib

1. urlopen
```py
In [4]: import urllib.request

In [5]: res = urllib.request.urlopen('http://www.baidu.com')  

"""
def urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            *, cafile=None, capath=None, cadefault=False, context=None):
加入data参数的话就是以post的形式请求
timeout 的参数，设置超时
"""

In [6]: print(res.read().decode('utf-8')) 

# 状态码、响应头

In [9]: print(res.status)
200

In [10]: print(res.getheaders())

In [12]: print(res.getheader('Server'))
BWS/1.1

In [13]: print(res.read().decode('utf-8'))  # 获取响应主体内容
```

2. Request
```py
In [14]: request = urllib.request.Request('http://www.baidu.com')

In [15]: res = urllib.request.urlopen(request)
```

3. 异常处理

> HTTPError 是 URLError 的父类

4. url解析

1. urlparse
```py
# def urlparse(url, scheme='', allow_fragments=True):

In [19]: from urllib.parse import urlparse

In [20]: res = urlparse('https://www.baidu.com/s?wd=python&rsv_spt=1&rsv_iqid=0xd39
    ...: fa189000111a9&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=98010089_dg&ch=14&
    ...: rsv_enter=1&rsv_sug3=2&rsv_sug1=2&rsv_sug7=101&rsv_sug2=0&inputT=3249&rsv_
    ...: sug4=3948&rsv_sug=1')

In [23]: print(type(res),'\n',res)
<class 'urllib.parse.ParseResult'> 
 ParseResult(scheme='https', netloc='www.baidu.com', path='/s', params='', query='wd=python&rsv_spt=1&rsv_iqid=0xd39fa189000111a9&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=98010089_dg&ch=14&rsv_enter=1&rsv_sug3=2&rsv_sug1=2&rsv_sug7=101&rsv_sug2=0&inputT=3249&rsv_sug4=3948&rsv_sug=1', fragment='')

# 可以urlparse('www.baidu.com', scheme='https') 传入， 如果前面有的，就使用前面的值，不会替换
 ```

 2. urlunparse 和 urlparse 相反，这个是拼接

 3. urljoin

```py
In [24]: from urllib.parse import urljoin

In [25]: print(urljoin('http://www.baidu.com','hello.html'))
http://www.baidu.com/hello.html

In [26]: print(urljoin('http://www.baidu.com','http://python.org'))
http://python.org 				# 域名不一样的话，后者覆盖前者

# 以后面的为基准填充
```

4. urlendecode

```py
In [27]: from urllib.parse import urlencode

In [28]: a = {'name':'l','age':40}

In [29]: base = 'www.baidu.com?'

In [30]: b = base + urlencode(a)

In [31]: print(b)
www.baidu.com?name=l&age=40
```

# requests

```py
In [1]: import requests

In [2]: res = requests.get('http://www.baidu.com')

In [3]: print(type(res))
<class 'requests.models.Response'>

In [4]: print(res.status_code)
200

In [5]: print(type(res.text))
<class 'str'>

In [6]: print(res.text)
<!DOCTYPE html>
<!--STATUS OK--><html> <head><meta http-equiv=content-type content=text/html;charset=utf-8><meta
...
In [7]: print(res.cookies)
<RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>
```

## 各种请求方式

1. request.get

```py
# 带参数
data = {
	'name': 'll',
	'age': 18,
}
res = request.get('http://www.baidu.com', params=data)   # 'http://www.baidu.com?name=ll&age=18'

# 解析json
print(res.json())   # json.loads(res.text)

# 获取二进制数据
print(res.content)

# 添加headers
headers = {
	......
}
res = request.get('http://www.baidu.com', headers=headers)
```

2. request.post

```py
res = request.post('http://www.baidu.com', data=data, headers=headers)
```

3. request.put

4. request.delete

5. request.head

6. request.options

## 响应

```py
In [12]: print(res.url)  	# 请求的url
http://www.baidu.com/

if requests.status_code == requests.codes.ok/not_found:  # 可以直接使用re	quests.codes.()判断
	pass

In [14]: print(type(res.history),res.history)		# 请求的历史
<class 'list'> []

In [15]: print(type(res.cookies),res.cookies)			# 请求的cookis
<class 'requests.cookies.RequestsCookieJar'> <RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>

In [16]: print(type(res.status_code),res.status_code)			# 请求的状态码
<class 'int'> 200

In [17]: print(type(res.headers),res.headers)			# 请求的头部
<class 'requests.structures.CaseInsensitiveDict'> {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Tue, 24 Jul 2018 12:05:08 GMT', 'Last-Modified': 'Mon, 23 Jan 2017 13:28:37 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18', 'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}
```

### 文件上传

```py
files = {'file': open('filename', 'rb')}
res = requests.post('url', files=files)
```

### 获取cookies

```py
In [1]: import requests

In [2]: res = requests.get('https://www.baidu.com')

In [3]: print(res.cookies)
<RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>

In [4]: for key,value in res.cookies.items():
   ...:     print(key + '=' + value)
   ...:     
BDORZ=27315
```

### 会话维持

```py
In [5]: s = requests.Session()

In [6]: s.get('http://httpbin.org/cookies/set/number/666')
Out[6]: <Response [200]>

In [7]: res = s.get('http://httpbin.org/cookies')

In [8]: print(res.text)
{
  "cookies": {
    "number": "666"
  }
}
```

### 忽略认证

```py
import requests
from requests.packages import urllib3
# urllib3.disable_warnings()
# res = requests.get('https://www.12306.cn', verify=False)
res = requests.get('https://www.12306.cn')
print(res.status_code)
```

### 设置代理

```py
import requests
proxies ={
    
}
res = requests.get(url, proxies=proxies)
print(res.status_code)

# :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
```

### 超时设置

```py
"""
参数 timeout
:param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
:type timeout: float or tuple
"""
```

### 异常处理

```py
from requests.exceptions import ReadTimeout, ConnectionError, RequestException

# ReadTimeout 超时错误
# ConnectionError 网络连接异常
```

# 正则

> re.S 匹配换行符模式
> /strip(), 取消换行符\n
> re.macth 从第一个字符串开始
> re.search 从所有的
> re.findall 找出所有的
> re.compile 复用，公式  sss= re.compile('', re.S) | re.match(sss, content)

1. re.sub(替换，返回替换后的)

```py
In [1]: import re

In [2]: a = 'hello world'

In [3]: res = re.sub('l', 'L', a)

In [4]: print(res)
heLLo worLd

In [5]: b = 'hello world , today is 2018-07-27'

In [6]: res1 = re.sub('\d', 'ceshi', b)

In [7]: print(res1)
hello world , today is ceshiceshiceshiceshi-ceshiceshi-ceshiceshi

In [8]: res2 = re.sub('\d+', 'ceshi', b)

In [9]: print(res2)
hello world , today is ceshi-ceshi-ceshi

In [10]: res3 = re.sub('(\d+)', r'\1ceshi', b)    # 注意这个写法

In [11]: print(res3)
hello world , today is 2018ceshi-07ceshi-27ceshi    # 保留原有的匹配字符串

```

# BeautifulSoup (推荐使用lxml解析库、find()、find_all()、select())


### 标签选择器
```py
In [1]: from bs4 import BeautifulSoup

a = """
  something
"""
In [3]: soup = BeautifulSoup(a, 'lxml')   

In [4]: print(soup.prettify())      # 补全网页，调整为标准格式

In [5]: print(soup.h1.string)       # 输出h1标签的信息   只返回选择的第一个
图书信息

In [9]: print(soup.h1)
<h1 style="color: #31b0d5;margin-left: 20px">图书信息</h1>

In [10]: print(type(soup.h1))
<class 'bs4.element.Tag'>

# 获取属性

In [11]: print(soup.h1.attrs['style'])
color: #31b0d5;margin-left: 20px


In [13]: print(soup.h1['style'])
color: #31b0d5;margin-left: 20px

# 子节点，列表

In [14]: print(soup.h3.contents)
['Python 3网络爬虫开发实战 ', <span class="label label-info">python</span>]

# 子节点，迭代器
In [15]: print(soup.h3.children)
<list_iterator object at 0x7f8918049128>

In [16]: for i in soup.h3.children:
    ...:     print(i)
    ...:     
Python 3网络爬虫开发实战 
<span class="label label-info">python</span>


# 所有的子孙节点
In [18]: print(soup.h3.descendants)
<generator object descendants at 0x7f89180ce410>

In [19]: for i in soup.h3.descendants:
    ...:     print(i)
    ...:     
Python 3网络爬虫开发实战 
<span class="label label-info">python</span>
python

# 父节点
In [20]: print(soup.span.parent)            
# 获取第一个span标签
# parents 获取所有的祖先节点
<h3 class="text-center">Python 3网络爬虫开发实战 <span class="label label-info">python</span></h3>

# 兄弟节点 （并列的节点）

In [23]: print(soup.span.next_siblings)
<generator object next_siblings at 0x7f89180ce2b0>

In [24]: print(soup.span.previous_siblings)
<generator object previous_siblings at 0x7f89180ce830>

```

### 标准选择器find_all（所有）、find（单个）

> 可根据标签名、属性、内容查找文档

```py

# 标签名

In [25]: print(soup.find_all('span'))
[<span class="label label-info">python</span>, <span style="color: #00dcf8">已出版</span>]

In [26]: print(type(soup.find_all('span')[0]))
<class 'bs4.element.Tag'>

# 属性（attrs）

In [30]: print(soup.find_all(attrs={'type':'button'}))
[<button class="btn btn-default pull-right" onclick="javascript:history.back(-1);" type="button"><i class="fa fa-history">返回上一页</i>
</button>]

# 文本内容（text）

In [34]: print(soup.find_all(text='python'))
['python']

```

### css选择器 select()

```py
In [35]: print(soup.select('span'))
[<span class="label label-info">python</span>, <span style="color: #00dcf8">已出版</span>]

In [36]: print(soup.select('.text-center'))    # (class == .)   (id == #)
[<h3 class="text-center">Python 3网络爬虫开发实战 <span class="label label-info">python</span></h3>]
```

### 获取属性

```py
In [38]: print(soup.select('.text-center')[0]['class'])
['text-center']

In [39]: print(soup.select('.text-center')[0].attrs['class'])
['text-center']
```

### 获取内容

```py
In [40]: print(soup.select('.text-center')[0].get_text())
Python 3网络爬虫开发实战 python
```

# pyquery

##  初始化

1. 字符串

```py
In [1]: import pyquery # ( from pyquery import PyQuery as pq )

In [2]: a = """<div class="new_nav">
   ...: <ul>
   ...: <li class="current"><a href="xxxxxx/" target="_self">首页</a></li>
   ...: <li><a href="xxxxxx/Dongzuodianying/">最新动作片</a></li>
   ...: <li><a href="xxxxxx/Kehuandianying/">最新科幻片</a></li>
   ...: <li><a href="xxxxxx/Kongbudianying/">最新恐怖片</a></li>
   ...: <li><a href="xxxxxx/Xijudianying/">最新喜剧片</a></li>
   ...: <li><a href="xxxxxx/Aiqingdianying/">最新爱情片</a></li>
   ...: <li><a href="xxxxxx/Juqingdianying/">最新剧情片</a></li>
   ...: <li><a href="xxxxxx/Zhanzhengdianying/">最新战争片</a></li>
   ...: <li class="dm"><a href="xxxxxx/Anime/">最新动漫</a></li>
   ...: <li class="dm"><a href="xxxxxx/Zuixinzongyi/">最新综艺</a></li>
   ...: </ul>
   ...: </div>"""

In [3]: doc = pyquery.PyQuery(a)

In [4]: print(doc('li'))
<li class="current"><a href="xxxxxx/" target="_self">首页</a></li>
<li><a href="xxxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxxx/Zuixinzongyi/">最新综艺</a></li>


In [5]: print(doc('a'))
<a href="xxxxxx/" target="_self">首页</a><a href="xxxxxx/Dongzuodianying/">最新动作片</a><a href="xxxxxx/Kehuandianying/">最新科幻片</a><a href="xxxxxx/Kongbudianying/">最新恐怖片</a><a href="xxxxxx/Xijudianying/">最新喜剧片</a><a href="xxxxxx/Aiqingdianying/">最新爱情片</a><a href="xxxxxx/Juqingdianying/">最新剧情片</a><a href="xxxxxx/Zhanzhengdianying/">最新战争片</a><a href="xxxxxx/Anime/">最新动漫</a><a href="xxxxxx/Zuixinzongyi/">最新综艺</a>

In [6]: print(doc('ul'))
<ul>
<li class="current"><a href="xxxxxx/" target="_self">首页</a></li>
<li><a href="xxxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxxx/Zuixinzongyi/">最新综艺</a></li>
</ul>
```

2. url 初始化

```py
In [7]: doc1 = pyquery.PyQuery(url='http://www.baidu.com')

In [8]: print(doc1('title'))
<title>ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é</title>
```

3. 文件初始化

```py
# doc2 = pyquery.PyQuery(filename='xxx.html')
```

## css选择器

```py
In [14]: print(doc('.current a'))
<a href="xxxxxx/" target="_self">首页</a>
```

## 子元素

```py
In [16]: print(doc.children('ul'))
<ul>
<li class="current"><a href="xxxxxx/" target="_self">首页</a></li>
<li><a href="xxxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxxx/Zuixinzongyi/">最新综艺</a></li>
</ul>

In [18]: print(doc.find('a'))
<a href="xxxxxx/" target="_self">首页</a><a href="xxxxxx/Dongzuodianying/">最新动作片</a><a href="xxxxxx/Kehuandianying/">最新科幻片</a><a href="xxxxxx/Kongbudianying/">最新恐怖片</a><a href="xxxxxx/Xijudianying/">最新喜剧片</a><a href="xxxxxx/Aiqingdianying/">最新爱情片</a><a href="xxxxxx/Juqingdianying/">最新剧情片</a><a href="xxxxxx/Zhanzhengdianying/">最新战争片</a><a href="xxxxxx/Anime/">最新动漫</a><a href="xxxxxx/Zuixinzongyi/">最新综艺</a>
```

## 父元素

```py
In [20]: doc2 = doc('li')

In [21]: print(doc2.parents())
<div class="new_nav">
<ul>
<li class="current"><a href="xxxxxxxx/" target="_self">首页</a></li>
<li><a href="xxxxxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxxxxx/Zuixinzongyi/">最新综艺</a></li>
</ul>
</div><ul>
<li class="current"><a href="xxxxxxxx/" target="_self">首页</a></li>
<li><a href="xxxxxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxxxxx/Zuixinzongyi/">最新综艺</a></li>
</ul>

In [22]: print(doc2.parent())
<ul>
<li class="current"><a href="xxxxxxxx/" target="_self">首页</a></li>
<li><a href="xxxxxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxxxxx/Zuixinzongyi/">最新综艺</a></li>
</ul>
```

## 兄弟元素

```py
In [24]: print(doc('.current').siblings())
<li><a href="xxxxx/Dongzuodianying/">最新动作片</a></li>
<li><a href="xxxxx/Kehuandianying/">最新科幻片</a></li>
<li><a href="xxxxx/Kongbudianying/">最新恐怖片</a></li>
<li><a href="xxxxx/Xijudianying/">最新喜剧片</a></li>
<li><a href="xxxxx/Aiqingdianying/">最新爱情片</a></li>
<li><a href="xxxxx/Juqingdianying/">最新剧情片</a></li>
<li><a href="xxxxx/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="xxxxx/Anime/">最新动漫</a></li>
<li class="dm"><a href="xxxxx/Zuixinzongyi/">最新综艺</a></li>
```

## 遍历

```py
In [29]: lis = doc3('.dm')

In [30]: print(lis)
<li class="dm"><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>
<li class="dm"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>


In [31]: lis = doc3('.dm').items()

In [32]: for i in lis:
    ...:     print(i)
    ...:     
<li class="dm"><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>

<li class="dm"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>
```

## 获取信息

```py
# 获取属性
In [34]: a = doc3('.dm a')

In [35]: print(a)
<a href="https://www.loldytt.com/Anime/">最新动漫</a><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a>

In [37]: print(a.attr('href'))      # 只能获取第一个
https://www.loldytt.com/Anime/

In [39]: print(a.attr.href)
https://www.loldytt.com/Anime/


# 获取文本
In [41]: print(a.text())
最新动漫 最新综艺

In [44]: print(a)
<a href="https://www.loldytt.com/Anime/">最新动漫</a><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a>

In [45]: print(a.html())
最新动漫

In [46]: print(doc2)
<li class="current"><a href="https://www.loldytt.com/" target="_self">首页</a></li>
<li><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>
<li><a href="https://www.loldytt.com/Kehuandianying/">最新科幻片</a></li>
<li><a href="https://www.loldytt.com/Kongbudianying/">最新恐怖片</a></li>
<li><a href="https://www.loldytt.com/Xijudianying/">最新喜剧片</a></li>
<li><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>
<li><a href="https://www.loldytt.com/Juqingdianying/">最新剧情片</a></li>
<li><a href="https://www.loldytt.com/Zhanzhengdianying/">最新战争片</a></li>
<li class="dm"><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>
<li class="dm"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>


In [47]: print(doc2.html())
<a href="https://www.loldytt.com/" target="_self">首页</a>

```

## DOM操作

1. removeClass
```py
In [48]: print(doc2.removeClass('dm'))
<li class="current"><a href="https://www.loldytt.com/" target="_self">首页</a></li>
<li><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>
<li><a href="https://www.loldytt.com/Kehuandianying/">最新科幻片</a></li>
<li><a href="https://www.loldytt.com/Kongbudianying/">最新恐怖片</a></li>
<li><a href="https://www.loldytt.com/Xijudianying/">最新喜剧片</a></li>
<li><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>
<li><a href="https://www.loldytt.com/Juqingdianying/">最新剧情片</a></li>
<li><a href="https://www.loldytt.com/Zhanzhengdianying/">最新战争片</a></li>
<li class=""><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>
<li class=""><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>
```
2. addClass
```py
In [49]: print(doc2.addClass('hello'))
<li class="current hello"><a href="https://www.loldytt.com/" target="_self">首页</a></li>
<li class="hello"><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Kehuandianying/">最新科幻片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Kongbudianying/">最新恐怖片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Xijudianying/">最新喜剧片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Juqingdianying/">最新剧情片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Zhanzhengdianying/">最新战争片</a></li>
<li class="hello"><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>
<li class="hello"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>
```
3. attr
```py
In [50]: print(doc2.attr('name','ppp'))
<li class="current hello" name="ppp"><a href="https://www.loldytt.com/" target="_self">首页</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Kehuandianying/">最新科幻片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Kongbudianying/">最新恐怖片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Xijudianying/">最新喜剧片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Juqingdianying/">最新剧情片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Zhanzhengdianying/">最新战争片</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>
<li class="hello" name="ppp"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>
```
4. css
```py
In [51]: print(doc2.css('color','red'))
<li class="current hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/" target="_self">首页</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Kehuandianying/">最新科幻片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Kongbudianying/">最新恐怖片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Xijudianying/">最新喜剧片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Juqingdianying/">最新剧情片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Zhanzhengdianying/">最新战争片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Anime/">最新动漫</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>
```
5. remove
```py
In [70]: s = """
    ...: <div>hello <p>HELLO</p> </div>
    ...: """

In [71]: doc = pyquery.PyQuery(s)

In [72]: print(doc.text())
hello
HELLO

In [74]: doc.find('p').remove()
Out[74]: []

In [75]: doc.text()
Out[75]: 'hello'

```

## 伪类选择器

```py
# 获取第一个

In [77]: print(doc2('li:first-child'))
<li class="current hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/" target="_self">首页</a></li>

# 获取最后一个
In [78]: print(doc2('li:last-child'))
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>

# 获取第二个
In [79]: print(doc2('li:nth-child(2)'))
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>

# 获取偶数
In [81]: print(doc2('li:nth-child(2n)'))
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Dongzuodianying/">最新动作片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Kongbudianying/">最新恐怖片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Zhanzhengdianying/">最新战争片</a></li>
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Zuixinzongyi/">最新综艺</a></li>

# 获取包含特定字符串的
In [82]: print(doc2('li:contains(爱情)'))
<li class="hello" name="ppp" style="color: red"><a href="https://www.loldytt.com/Aiqingdianying/">最新爱情片</a></li>

# 获取大于特定数字的
In [84]: print(doc2('li:gt(2)'))

In [85]: print(doc2('li:lt(2)'))

```

# Selenium

> 自动化测试工具，支持多种浏览器，爬虫中解决JavaScript的渲染问题