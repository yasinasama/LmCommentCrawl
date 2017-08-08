import re
import requests
from bs4 import BeautifulSoup
import MySQLdb



# max 99
PAGE_COUNT = 99
PRODUCT_url = 'https://detail.tmall.com/item.htm?id=524532438541&abbucket=1&skuId=3557354651778'
TAG_TRL = 'https://rate.tmall.com/listTagClouds.htm?itemId=524532438541&isAll=true&isInner=true'

re_item = re.compile('"rateContent":"(.*?)","rateDate":"(.*?)"')
re_tag = re.compile('"id":"(.*?)","tag":"(.*?)"')

def getCrawlUrl(page, tag):
    return 'https://rate.tmall.com/list_detail_rate.htm?itemId=12601223455&sellerId=628189716&order=3&currentPage=%s&tagId=%s' % (page, tag)


def getConn():
    try:
        return MySQLdb.connect(host='172.16.10.95', port=3306, user='bcw', passwd='bcw@517', db='bcw_comments')
    except Exception as e:
        raise e


req_product = requests.get(PRODUCT_url)
soup = BeautifulSoup(req_product.text, "html.parser")


for i in range(1):
    conn = getConn()
    cs = conn.cursor()
    req = requests.get(getCrawlUrl(i, '3337'))
    item = re.findall(re_item, req.text)
    for j in range(len(item)):
        product_code = '1212121'
        product_name = '碧根果'
        comment_content = item[j][0]
        comment_time = item[j][1]
        cs.execute('INSERT INTO comments VALUES(%s,%s,%s,%s) ' % (product_code, product_name, comment_content, comment_time))
        cs.commit()

    cs.close()
    conn.close()


