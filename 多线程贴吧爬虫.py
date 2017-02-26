#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import urllib
import time
import multiprocessing
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
    "Cookie":"TIEBA_USERTYPE=f5b3af10c72414574c46106f; bdshare_firstime=1469268550290; TIEBAUID=9c0c5e238b095b0c4c1efa61; rpln_guide=1; BDUSS=GJzbU0tNnJOY0toM0xXTFJsSjFrMER0NHRuZEMxRFFWQjJaTFZKbDhlZExHZXBYQVFBQUFBJCQAAAAAAAAAAAEAAAChfcIRs~7stsu5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEuMwldLjMJXb; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1474630150,1474631449,1474776888; BAIDUID=D9ADA052E8F2D21C5FF0C469536DC5AE:FG=1; PSTM=1477225027; BIDUPSID=1FDE40D4D51192045C644DDD902D2677; __cfduid=d7b69e4ac28c7535b69b645bd7a8b94311481117304; STOKEN=81785a1a09b324efed40b602d990cf8e94fc5c1184ef9fc46dcda31bd2599760; wise_device=0; PSINO=1; H_PS_PSSID=1440_21108_21312_22035_22025; LONGID=297958817"
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

if __name__=="__main__":
    url_tieba="http://tieba.baidu.com/f/like/furank?kw=%D3%A2%D0%DB%D6%BE&pn={}"
    n=21
    urls=requests_tieba(url_tieba, n)
    main(urls)
