# -*- coding: utf-8 -*-
import os
from os.path import basename
import re
import time
import urllib2
from urlparse import urlsplit
from bs4 import BeautifulSoup
from selenium import webdriver
import RandomProxyIp
import facepp

def init(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)

def load_total_answer_num(pre_url):
    url_content = urllib2.urlopen(pre_url).read()
    soup = BeautifulSoup(url_content,'lxml')
    h4 = soup.find_all(class_ = "List-headerText")[0]
    a = re.findall("(\d?)", h4.span.string.encode('utf8'))
    num = ''
    for i in a:
        if i:
            num += i
    return  int(num)

def prase_html(html, ONLY_FEMALE = False):
    soup = BeautifulSoup(html, 'lxml')
    t1 = soup.find_all('noscript')
    img_urls = []
    for t2 in t1:
        img_url_b = re.findall('src="(.*_b\..*?)"', str(t2))[0]
        img_url_r = ''
        try:
            img_url_r = '' + re.findall('data-original="(.*_r\..*?)"', str(t2))[0]
        except:
            pass
        
        if ONLY_FEMALE :
            p = facepp.Facepp('FR2qXQzf**************D8h_sVIx','0M7jG1*************UWD91C-')
            print img_url_b
            if p.has_female(img_url_b):
                if img_url_r:   #如果有原图，则优先选用原图
                    img_urls.append(img_url_r)
                else:
                    img_urls.append(img_url_b)
        else:        
            if img_url_r:   #如果有原图，则优先选用原图
                img_urls.append(img_url_r)
            else:
                img_urls.append(img_url_b)
            
    return img_urls

def save_pic(img_urls, filepath):
    for img_url in img_urls:
        try:
            img_data = urllib2.urlopen(img_url).read()
            file_name = basename(urlsplit(img_url)[2])
            output = open(filepath + '/' + file_name, 'wb')
            output.write(img_data)
            output.close()
        except:
            pass  
          
def main():
    question_id = '37787176'
    ONLY_FEMALE = True #仅挑出有女生人脸的图片
    
    filepath = 'images' + question_id
    init(filepath)
    pre_url = 'https://www.zhihu.com/question/' + question_id
    limits = load_total_answer_num(pre_url)
    page_size = 20
    page = 20
    while page <= (limits/page_size + 1):
        webdriver.ChromeOptions().add_argument('--proxy-server={0}'.format(RandomProxyIp.ProxyIp().get_random_proxy_ip()))
        driver = webdriver.Chrome()
        url = pre_url + '/answers/created??page=' + str(page)
        print '当前页面 : ' + url      
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        html = driver.page_source.encode('utf8')
        img_urls = prase_html(html, ONLY_FEMALE = ONLY_FEMALE)
        save_pic(img_urls, filepath)
        page += 1
        driver.close()
    print 'Done.'
    
main()      
