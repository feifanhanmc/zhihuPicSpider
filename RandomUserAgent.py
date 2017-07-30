# -*- coding: utf-8 -*-
from fake_useragent import UserAgent

def random_user_agent():
    '''
        目前有个问题是：这里面给出的User-Agent所代表的浏览器有的版本过低，不能正常访问网页
    :return A random User-Agent(str). 
    '''
    ua = UserAgent()
    return ua.random.encode('utf8')