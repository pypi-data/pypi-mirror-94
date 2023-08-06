import requests
import parsel
import re 
import json
import pandas as pd
from bs4 import BeautifulSoup
from goose3 import Goose
from goose3.text import StopWordsChinese
from newspaper import Article
class slycrawl(object):
    def __init__(self,url='',headers={},params={}):
        response=requests.get(url,headers=headers,params=params)
        response.encoding=response.apparent_encoding
        self.response=response
        self.url=response.url
        self.headers=response.headers
        self.cookies=response.cookies
        self.html=response.text
    def get_html(self):
        return self.response.text
    def get_selector(self):
        return parsel.Selector(self.response.text)
    def get_json(self):
        return json.loads(self.response.text)
    def get_proxy(self,number=1):
        proxies=[]
        for i in range(number):
            url = 'http://118.24.52.95/get/'
            json_data = requests.get(url=url).json()
            proxy = json_data['proxy']
            proxies.append({
                "http": "http://" + proxy,
                "https": "https://" + proxy,
            })
        return proxies
    def get_soup(self):
        return BeautifulSoup(self.response.text,'html.parser')
    def get_text(self,useragent='',accurate=True):
        try:    
            if accurate == True:
                g = Goose({'stopwords_class': StopWordsChinese,
                        'browser_user_agent': useragent
                        })
            else:
                g = Goose({'browser_user_agent': useragent
                        })
            article=g.extract(url=self.url)
            dic={
            'title':article.title,#标题
            'text':article.cleaned_text,#正文
            'description':article.meta_description,#摘要
            'keywords':article.meta_keywords,#关键词
            'tags':article.tags,#标签
            'image':article.top_image,#主要图片
            'infomation':article.infos,#包含所有信息的 dict
            'raw_html':article.raw_html#原始 HTML 文本
            }
            return dic
        except Exception as e:
            print(e)
    def get_news(self):
        news = Article(self.url, language='zh')
        news.download()
        news.parse()
        dicts={}
        dicts['text']=news.text
        dicts['title']=news.title
        dicts['html']=news.html
        dicts['author']=news.authors
        dicts['image']=news.top_image
        dicts['movies']=news.movies
        dicts['keywords']=news.keywords
        dicts['summary']=news.summary
        return dicts   
    def get_links(self):
        links = re.findall('"((http|ftp)s?://.*?)"', self.html)
        links=[i[0] for i in links]
        return links
    def get_tables(self):
        df=pd.read_html(self.url)
        return df
