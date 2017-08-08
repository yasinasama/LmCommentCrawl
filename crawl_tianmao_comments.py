import re
import requests
import MySQLdb


# max 99
PAGE_COUNT = 99
PRODUCT_URL = 'https://detail.tmall.com/item.htm?id=524532438541&abbucket=1&skuId=3557354651778'
TAG_TRL = 'https://rate.tmall.com/listTagClouds.htm?itemId=524532438541&isAll=true&isInner=true'

re_item = re.compile('"rateContent":"(.*?)","rateDate":"(.*?)"')
re_tag = re.compile('"id":"(.*?)".*?"tag":"(.*?)"')
re_b = re.compile('</?b>')

def getTagUrl(id):
    return 'https://rate.tmall.com/listTagClouds.htm?itemId=%s&isAll=true&isInner=true' % id


tag_req = requests.get(TAG_TRL)
tag_item = re.findall(re_tag, tag_req.text)


def getCrawlUrl(page, tag):
    return 'https://rate.tmall.com/list_detail_rate.htm?itemId=12601223455&sellerId=628189716&order=3&currentPage=%s&tagId=%s' % (page, tag)


def getConn():
    try:
        return MySQLdb.connect(host='172.16.10.95', port=3306, user='bcw', passwd='bcw@517', db='bcw_comments')
    except Exception as e:
        raise e

conn = getConn()
cs = conn.cursor()
for t in range(len(tag_item)):
    for i in range(6):
        req = requests.get(getCrawlUrl(page=i+1, tag=tag_item[t][0]))
        item = re.findall(re_item, req.text)
        for j in range(len(item)):
            print(item[j])
            product_code = '1212121'
            product_name = '碧根果'
            comment_content = item[j][0]
            comment_time = item[j][1]
            cs.execute('INSERT INTO comments VALUES(%s,%s,%s,%s) ' % (product_code, product_name, comment_content, comment_time))
            cs.commit()

cs.close()
conn.close()


