#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import urllib
import time
import multiprocessing
headers={
    "User-Agent":"",
    "Cookie":""
}

def get_url(url_tieba,n):
    urllist=[url_tieba.format(i) for i in range(17,n)]
    return urllist
    #获取网址列表
def requests_tieba(url_tieba,n):
    url_list=get_url(url_tieba,n)
    geren_urllist=[]
    for url in url_list:
        soup=getrequest(url)
        titles=soup.select("a.drl_item_name_nor")
        for link in titles:
            geren = link.get("username")
            gerenid = link.get_text()
            # 此处第一页的三个名字无法获取到
            geren_url = "http://tieba.baidu.com/home/main/?un={}&fr=furank".format(geren)
            geren_urllist.append(geren_url)
    return geren_urllist
    #print(geren_urllist)
def getrequest(url):
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,"html.parser")
    return soup
    #请求函数

def geren_pic(url):
    soup = getrequest(url)
    titles = soup.select("#userinfo_wrap > div.userinfo_middle > div.userinfo_title > span")
    titles_tx=soup.select("a.userinfo_head")
    if len(titles)==0:
        print(url+"page404")
    else:
        for link in titles:
            name=link.get_text()
        for links in titles_tx:
            tx=links.img["src"]
        path = "d:\\py\\pc\\tieba\\123\\"+ name + ".jpg"
        urllib.request.urlretrieve(tx, path)
        print("下载成功")

def main(urls):
    pool=multiprocessing.Pool(multiprocessing.cpu_count())
    for url in urls:
        pool.apply_async(geren_pic,(url,))
    pool.close()
    pool.join()
    #获取cpu数，多进程爬取
if __name__=="__main__":
    url_tieba="http://tieba.baidu.com/f/like/furank?kw=%D3%A2%D0%DB%D6%BE&pn={}"
    n=21
    urls=requests_tieba(url_tieba, n)
    main(urls)
