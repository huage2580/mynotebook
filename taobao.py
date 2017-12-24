from http import cookiejar

from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import json
import re
import http.cookiejar
import time
import prettytable
# url = 'https://s.taobao.com/search?q=%s&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc'
# url = url % urllib.parse.quote('小鸡')
# url = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId=559743541426'
# request = urllib.request.Request(url)
# request.add_header('Referer', 'https://detail.tmall.com/item.htm?id=559743541426')
# response = urllib.request.urlopen(request)
# html = response.read().decode('gbk')
# json = json.loads(html)
# soup = BeautifulSoup(html, 'lxml')
# print(json['defaultModel']['sellCountDO']['sellCount'])
# for link in soup.find_all('a'):
#     print(link.get('href'))

# 搜索关键词
keyword = '小鸡手柄'
# 型号过滤
models = ('f1', 'g3', 'g4', 't1')
# 存储价格的dict
prices = dict()
# 存储销量
sales_count = dict()

# 全局代理设置
# proxy_support = urllib.request.ProxyHandler({'http': '127.0.0.1:1080'})
# opener = urllib.request.build_opener(proxy_support)
# opener.addheaders = [('User-Agent','Test_Proxy_Python3.5_maminyao')]
# urllib.request.install_opener(opener)

cookie = cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)


def save_prices(model, p):
    if model not in prices:
        prices[model] = int(float(p))


def save_sales(model,count):
    if not model == 'none':
        old = sales_count.get(model, 0)
        sales_count[model] = old+count


def title2model(title):
    for model in models:
        re_result = re.search(model, title, re.I)
        if re_result:
            return model
    return 'none'


def get_detail_sale(nid):
    detial_url = 'https://mdskip.taobao.com/core/initItemDetail.htm?itemId=%s' % nid
    md_url = 'https://detail.m.tmall.com/item.htm?spm=a220m.6910245.0.0.11088e1dizFxq2&id=%s&skuId=3471118795556' % nid
    md_re = r'sellCount\":(\d*)'
    ref = 'https://detail.tmall.com/item.htm?id=%s' % nid
    respone_text = ''
    while respone_text == '':
        print('try into detail', nid)
        request = urllib.request.Request(md_url)
        request.add_header('Referer', ref)
        respone = urllib.request.urlopen(request)
        respone_text = respone.read().decode('gbk')
    result = re.search(md_re, respone_text, re.I|re.M)
    if result:
        return result.group(1)
    return ''


def ensure_sale(is_tmail, nid, sale):
    count = re.match(r'(\d*).*', sale).group(1)
    if not is_tmail:
        return count
    else:
        es = get_detail_sale(nid)
        if not es == '':
            return es
        return count


# 随便进入下淘宝
urllib.request.urlopen('https://www.taobao.com/').read()
# 搜索关键词获取列表
search_url = 'https://s.taobao.com/search?data-key=sort&data-value=sale-desc&ajax=true&_ksTS=1514015244325_2253&callback=&q=%s&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=renqi-desc' % urllib.parse.quote(keyword)
json_text = ''
while json_text == '':
    print('try to search keyword...', keyword)
    request = urllib.request.Request(search_url)
    search_reponse = urllib.request.urlopen(request)
    json_text = search_reponse.read().decode('utf-8')
item_list = json.loads(json_text)['mods']['itemlist']['data']['auctions']

for item in item_list:
    title = item['raw_title']
    nid = item['nid']
    price = item['view_price']
    sale = item['view_sales']
    shop = item['nick']
    is_tmail = item['shopcard']['isTmall']
    model = title2model(title)
    save_prices(model, price)
    sale_int = int(ensure_sale(is_tmail, nid, sale))
    save_sales(model, sale_int)
    # print(title,model,sale_int)

# 表格输出
table = prettytable.PrettyTable(["model", "price", "sales", "money"])
all_money = 0
for item in sales_count:
    all_money += prices[item]*sales_count[item]
    table.add_row([item, prices[item], sales_count[item], prices[item]*sales_count[item]])
table.add_row(['ALL', '', '', "{:,}".format(all_money)])
table.align = 'r'
print(table)




