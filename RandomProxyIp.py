# -*-coding: utf-8 -*-
import re
import random
import mangedb
import requests
from RandomUserAgent import random_user_agent
from bs4 import BeautifulSoup

class ProxyIp():
    '''
       调用时直接 使用proxies = RandomProxyIp.ProxyIp().get_random_proxy_ip()即可。
       数据库中没有代理ip可以用时，会自动通过crawl_ips()获取，当然也可以手动直接通过crawl_ips()获取。
    '''
    def __init__(self):
#         self.reset_db_table()
        return
    
    def reset_db_table(self):
        db = mangedb.Database('mytest')
        db.create_table('proxy_ip', "CREATE TABLE proxy_ip(IP VARCHAR(15) PRIMARY KEY, \
                        PORT VARCHAR(10), PROXY_TYPE VARCHAR(10), SPEED VARCHAR(10),\
                        SURIVE_TIME VARCHAR(10), CERTIFY_DATE VARCHAR(20))")

    def prase_html(self,soup):
        ip_list = []
        table = soup.find_all(id='ip_list')[0]
        #第一个tr项是title，国家    IP地址    端口    服务器地址    是否匿名    类型    速度    连接时间    存活时间    验证时间
        tr_list = table.find_all('tr')[1:]  
        for tr in tr_list:
            td_list = tr.find_all('td')
            ip = td_list[1].string.strip().encode('utf8')
            port = td_list[2].string.strip().encode('utf8')
            proxy_type = td_list[5].string.strip().encode('utf8')
            speed = re.findall('(\d*\.\d*).*', td_list[6].find_all('div', class_ = 'bar')[0].attrs['title'].encode('utf8'))[0]
            surive_time = td_list[8].string.strip().encode('utf8')
            certify_date = td_list[9].string.strip().encode('utf8')
            if surive_time.endswith('天') and float(speed) < 1.0:   #选取一些质量比较高的ip
                ip_list.append((ip, port, proxy_type, speed, surive_time, certify_date))
        return ip_list
        
    def crawl_ips(self):
        #爬取西刺网的免费代理IP
        total_ip_num = len(self.get_db_ip())
        max_ip_num = 30
        total_page_num = 1
        page = 1
        while (page <= total_page_num) and (total_ip_num < max_ip_num):
            print '正在爬取第' + str(page) + '页，已获取ip共 : ' + str(total_ip_num) + '个'
            url = 'http://www.xicidaili.com/nn/' + str(page)
            headers = {'User-Agent': random_user_agent()}
            
            if total_ip_num == 0:    #如果数据库中没有代理ip，则首次爬取代理ip时不可能调用数据库里的代理ip
                proxies = {}
            else:
                proxies=self.get_random_proxy_ip()
            r = requests.get(url, headers=headers, proxies=proxies)
            
            soup = BeautifulSoup(r.text,"lxml")
            ip_list = self.prase_html(soup)
            
            
            db = mangedb.Database('mytest')
            db.save_data('proxy_ip', ['ip', 'port', 'proxy_type', 'speed', 'surive_time', 'certify_date'], ip_list[0:max_ip_num-total_ip_num])
            
            total_ip_num += len(ip_list)
            if page == 1:
                total_page_num = int(soup.find_all(class_ = 'pagination')[0].find_all('a')[-2].string.encode('utf8').strip())
            page += 1
        
        if total_ip_num == max_ip_num:
            print '已爬取足够的代理ip，现在可以通过get_random_proxy_ip()获取代理ip'
            
    def delete_ip(self, ip):
        '''
                从数据库中删除无效的IP 
        '''
        print '正在删除无效ip : ' + ip
        db = mangedb.Database('mytest')
        flag = db.execute("""DELETE FROM proxy_ip WHERE ip='{0}'""".format(ip))
        if flag:
            print '删除ip : ' + ip + '成功'
    
    def judge_ip(self, ip, port):
        '''
                判断IP是否可用
        '''
        http_url = "http://www.baidu.com"
        proxies = {"http": "http://{0}:{1}".format(ip, port)}
        print '------------------------------------------------'
        print '正在验证ip : ' + ip + ':' + port
        try:
            response = requests.get(http_url, proxies = proxies)
        except Exception,e:
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                return True
            else:
                return False
    
    def get_db_ip(self):
        db = mangedb.Database('mytest')
        results = db.raw_select("SELECT ip, port FROM proxy_ip")
        return results
    
    def get_random_ip(self):
        results = self.get_db_ip()
        
        #如果数据库中没有ip可用，则重新爬取
        if len(results) == 0:
            return self.crawl_ips()
        
        for i in range(len(results)):
            ip_info = random.choice(results)
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                print '验证通过'
                return "http://{0}:{1}".format(ip, port)
            else:
                print '验证失败'
                self.delete_ip(ip)
                return self.get_random_ip()
    
    def get_random_proxy_ip(self):
        proxies = {"http" : self.get_random_ip()}
        return proxies
    
# if __name__ == "__main__":
#     p = ProxyIp()
#     p.crawl_ips()