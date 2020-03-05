import json
import re
import requests
from ProxyPool.proxypool.utils import get_page, get_page_noverify
from ProxyPool.proxypool.proxypool_log import print_messege

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print_messege('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies
    '''
    def crawl_xundaili(self):
        start_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=66a631eeea7a4e06b633b6005f4c00df&orderno=YZ20202112612qRHV5B&returnType=2&count=10'
        html = get_page(start_url)
        html_json = json.loads(html)
        ip_list = html_json['RESULT']
        for ip in ip_list:
            address_port = 'http://' + ip['ip'] + ':' + ip['port']
            yield address_port.replace(' ','')

    # 可以爬取
    def crawl_zdaye(self):
        start_url = 'https://www.zdaye.com/dayProxy/1.html'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        requests.packages.urllib3.disable_warnings()
        html = requests.get(start_url, headers=headers, verify=False)
        html = html.text
        if html:
            find_url = re.compile('href="/dayProxy/ip/(.*?).*?l')
            id = find_url.search(html)
            id = int(id.group(0)[19:25])
            for i in range(id-2,id+1):
                url = 'https://www.zdaye.com/dayProxy/ip/' + str(i) + '.html'
                response = get_page_noverify(url,options=headers)
                #print(response)
                find_ip_port = re.compile('<br>.(\d+.*?)@', re.S)
                re_ip_port = find_ip_port.findall(response)
                for ip_port in re_ip_port:
                    address_port = 'http://' + ip_port
                    yield address_port.replace(' ','')
    '''

    #只能爬第一页，之后503无法爬取
    def crawl_kuaidaili(self):
        for i in range(1, 2):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                #ip_type = re.compile('<td data-title="类型">(.*?)</td>', re.S)
                #re_ip_type = ip_type.findall(html)
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = 'http://' + address + ':' + port
                    yield address_port.replace(' ','')

    #可以爬取
    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host':'www.xicidaili.com',
                'Referer':'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests':'1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>') 
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    #find_type = re.compile('<td class="country">高匿</td>.*?<td>(.*?)</td>', re.S)
                    #re_ip_type = find_type.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = 'http://' + address + ':' + port
                        yield address_port.replace(' ','')
    #可以爬取
    def crawl_ip3366(self):
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    #find_type = re.compile('<td>.*?IP</td>.*?<td>(.*?)</td>', re.S)
                    #re_ip_type = find_type.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = 'http://' + address+ ':' +port
                        yield address_port.replace(' ','')

    #只能爬取第一页，之后503
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page_noverify(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                #find_type = re.compile('<td>.*?(HTTP\S).*?</td>', re.S)
                #re_ip_type = find_type.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    address_port = 'http://' + address+':'+port
                    yield address_port.replace(' ','')

    # 失效
    '''
    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])
    '''

    #失效
    '''
    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')
    '''

            