# 爬取 http://quotes.toscrape.com/

1. 抓取第一页，得到源代码，分析
2. 提取首页内容，获取下一页链接
3. 翻页爬取
4. 保存爬取结果，存储


## 保存方式

scrapy crawl name -o ...(ftp://user.passwd@ftp.example.com/path/quotes.csv)

# scrapy 命令行（https://docs.scrapy.org/en/latest/topics/commands.html）

1. scrapy startproject testproject  开始项目
2. scrapy genspider name url   # 生成spider
3. scrapy genspider -l    输出模板
4. scrapy genspider -t muban name url    指定生成的
5. scrapy crawl name  爬取
6. scrapy check    检查代码
7. scrapy list     返回项目里所有爬虫的名称
8. scrapy fetch --nolog --headers url
9. scrapy view url    调用浏览器打开
10. scrapy shell url    shell 模式
11. scrapy runspider filename       运行
12. scrapy version -v       输出依赖环境


### scrapy selectors

1. 基本用法
```py
# scrapy shell https://doc.scrapy.org/en/latest/_static/selectors-sample1.htm

In [1]: response.selector
Out[1]: <Selector xpath=None data='<html>\n <head>\n  <base href="http://exam'>

In [3]: response.selector.xpath('//title/text()')
Out[3]: [<Selector xpath='//title/text()' data='Example website'>]

In [4]: response.selector.xpath('//title/text()').extract_first()
Out[4]: 'Example website'

In [5]: response.selector.css('title::text').extract_first()
Out[5]: 'Example website'

In [6]: response.selector.css('title::text')
Out[6]: [<Selector xpath='descendant-or-self::title/text()' data='Example website'>]

# Querying responses using XPath and CSS is so common that responses include two convenience shortcuts: response.xpath() and response.css()
# 可以不用写selector

In [8]: response.css('title::text').extract_first()
Out[8]: 'Example website'		

In [9]: response.xpath('//title/text()').extract_first()
Out[9]: 'Example website'

# -------------------------------------------------------------------------------

In [10]: response.xpath('//div[@id="images"]')
Out[10]: [<Selector xpath='//div[@id="images"]' data='<div id="images">\n   <a href="image1.htm'>]

In [11]: response.xpath('//div[@id="images"]').css('img')
Out[11]: 
[<Selector xpath='descendant-or-self::img' data='<img src="image1_thumb.jpg">'>,
 <Selector xpath='descendant-or-self::img' data='<img src="image2_thumb.jpg">'>,
 <Selector xpath='descendant-or-self::img' data='<img src="image3_thumb.jpg">'>,
 <Selector xpath='descendant-or-self::img' data='<img src="image4_thumb.jpg">'>,
 <Selector xpath='descendant-or-self::img' data='<img src="image5_thumb.jpg">'>]

In [12]: response.xpath('//div[@id="images"]').css('img::attr(src)')
Out[12]: 
[<Selector xpath='descendant-or-self::img/@src' data='image1_thumb.jpg'>,
 <Selector xpath='descendant-or-self::img/@src' data='image2_thumb.jpg'>,
 <Selector xpath='descendant-or-self::img/@src' data='image3_thumb.jpg'>,
 <Selector xpath='descendant-or-self::img/@src' data='image4_thumb.jpg'>,
 <Selector xpath='descendant-or-self::img/@src' data='image5_thumb.jpg'>]

In [14]: response.xpath('//div[@id="images"]').css('img::attr(src)').extract()
Out[14]: 
['image1_thumb.jpg',
 'image2_thumb.jpg',
 'image3_thumb.jpg',
 'image4_thumb.jpg',
 'image5_thumb.jpg']

# 设置 default ，如果没有找到就返回指定的内容
 In [16]: response.xpath('//div[@id="images"]').css('img::attr(srcww)').extract_first(default="nothing
    ...:  to show")
Out[16]: 'nothing to show'

In [18]: response.xpath('//a/@href')
Out[18]: 
[<Selector xpath='//a/@href' data='image1.html'>,
 <Selector xpath='//a/@href' data='image2.html'>,
 <Selector xpath='//a/@href' data='image3.html'>,
 <Selector xpath='//a/@href' data='image4.html'>,
 <Selector xpath='//a/@href' data='image5.html'>]

In [20]: response.xpath('//a/@href').extract()
Out[20]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

In [24]: response.css('a::attr(href)').extract()
Out[24]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

In [25]: response.css('a::text').extract()
Out[25]: 
['Name: My image 1 ',
 'Name: My image 2 ',
 'Name: My image 3 ',
 'Name: My image 4 ',
 'Name: My image 5 ']

In [26]: response.xpath('//a/text()').extract()
Out[26]: 
['Name: My image 1 ',
 'Name: My image 2 ',
 'Name: My image 3 ',
 'Name: My image 4 ',
 'Name: My image 5 ']
```

2. 查询包含某个属性的标签

```py
In [28]: response.xpath('//a[contains(@href, "5")]/@href').extract()
Out[28]: ['image5.html']

In [31]: response.css('a[href*=image]::attr(href)').extract()
Out[31]: ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

In [32]: response.css('a[href*=image5]::attr(href)').extract()
Out[32]: ['image5.html']
# 直接 a[href*=5] 会报错

# 获取里面的 img 的 src 属性
In [35]: response.xpath('//a[contains(@href, "5")]/img/@src').extract()
Out[35]: ['image5_thumb.jpg']

In [36]: response.css('a[href*=image5] img::attr(src)').extract()
Out[36]: ['image5_thumb.jpg']
```

3. 正则表达式的匹配
```py
In [39]: response.css('a::text').re('Name\:(.*)')
Out[39]: 
[' My image 1 ',
 ' My image 2 ',
 ' My image 3 ',
 ' My image 4 ',
 ' My image 5 ']

In [40]: response.css('a::text').re_first('Name\:(.*)')
Out[40]: ' My image 1 '
```

# spiders 用法

1. custom_settings 覆盖settings的全局配置

2. start_request():
默认使用的是get请求，可以改写
If you want to change the Requests used to start scraping a domain, this is the method to override. For example, if you need to start by logging in using a POST request, you could do:
```py
class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        return [scrapy.FormRequest("http://www.example.com/login",
                                   formdata={'user': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]

    # yield scrapy.Request(url='', method='POST', call_back=)

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass
```

# Item Pipeline

1. process_item(self, item, spider)

> This method is called for every item pipeline component. return a dict with data, return an Item (or any descendant class) object, return a Twisted Deferred or raise DropItem exception.

```py
def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)
```   

2. from_crawler  获取settings 里的全局配置， 传递给init

3. open_spider		在spider开启

4. close_spider			关闭时

5. 优先级的设置，settings

```py
ITEM_PIPELINES = {
   # 'quotetutorial.pipelines.QuotetutorialPipeline': 300,
   'quotetutorial.pipelines.MongoPipeline': 400,
}
```

# Downloader Middleware(下载中间件)

1. scrapy settings --get=DOWNLOADER_MIDDLEWARES_BASE   查看基本的中间件及优先级



# 实战： 爬取知乎用户的信息

### 流程：

1. 选定起始人

2. 通过知乎接口获得其粉丝列表和关注列表

3. 获取列表中的用户的信息

4. 进一步获取

### tushare (财经数据接口)[http://tushare.org/]


# scrapy 分布式原理

## redis 队列

1. 非关系型数据库， key-value 形式存储，结构灵活
2. 是内存中的数据结构存储系统，处理速度快，性能好
3. 提供队列、集合等多种存储结构，方便队列的维护

4. 怎么完成去重： redis集合

> redis 提供集合数据结构，在redis 集合存储每个request 的指纹。 在向request队列中加入request前首先验证这个request的指纹是否已经加入集合。如果存在则不添加到队列；如果不存在则加入队列并将指纹加入集合。

5. 怎么防止中断：启动判断

> 在每台从机scrapy启动时都会先判断当前redis request队列是否为空。如果不为空，则从队列中去的下一个request执行爬取；如果为空，则重新开始爬取，第一台从机执行爬取想队列中添加request。


## scrapy-redis


## scrapyd 分布式部署

scrapyd-client
python-scrapyd-api


### git

1. 新建分支
```
git checkout -b <branch-name>   # -b 指定分支，clone也需要；push 需要 push -u origin <branch-name>
```

