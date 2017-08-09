import re
import requests
import MySQLdb
import datetime
import time
import math

# max 99
MAX_TAG_PAGE_COUNT = 99
PRODUCT_URL = 'https://detail.tmall.com/item.htm?id=524532438541&abbucket=1&skuId=3557354651778'
TAG_URL = 'https://rate.tmall.com/listTagClouds.htm?itemId=524532438541&isAll=true&isInner=true'
PRODUCT_CODE = '12601223455'
PRODUCT_NAME = '百草味-卤香鹌鹑蛋128g'


re_item = re.compile('"rateContent":"(.*?)","rateDate":"(.*?)"')
re_tag = re.compile('"count":(.*?),"id":"(.*?)".*?"tag":"(.*?)"')

# tag下的页数 max为99
def tagPageCount(total_item):
    pages = math.ceil(total_item / 20)
    return pages if pages <= MAX_TAG_PAGE_COUNT else MAX_TAG_PAGE_COUNT

# tag标签URL
def getTagUrl(id):
    return 'https://rate.tmall.com/listTagClouds.htm?itemId=%s&isAll=true&isInner=true' % id


# 店铺为百草味
def getCrawlUrl(id, page, tag):
    return 'https://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=628189716&order=1&currentPage=%s&tagId=%s' % (id, page, tag)


def getConn():
    try:
        return MySQLdb.connect(host='172.16.10.95', port=3306, user='bcw', passwd='bcw@517', db='bcw_comments', use_unicode=True, charset='utf8')
    except Exception as e:
        raise e


tag_req = requests.get(TAG_URL)
tag_item = re.findall(re_tag, tag_req.text)

conn = getConn()
cs = conn.cursor()

for t in range(len(tag_item)):
    tagcount = tagPageCount(int(tag_item[t][0]))
    print('开始抓取 %s 下的评论.............................' % tag_item[t][2])

    for i in range(tagcount):
        req = requests.get(getCrawlUrl(id=524532438541, page=i + 1, tag=tag_item[t][1]))
        item = re.findall(re_item, req.text)
        print('开始抓取第%d页的评论........................................' % (i + 1))
        for j in range(len(item)):
            product_code = PRODUCT_CODE
            product_name = PRODUCT_NAME
            comment_content = re.sub('</?b>', '', item[j][0])
            print(comment_content)
            comment_time = datetime.datetime.strptime(item[j][1],'%Y-%m-%d %H:%M:%S')
            cs.execute('INSERT INTO comments(ProductCode, ProductName, CommentContent, CommentTime) VALUES("%s","%s","%s","%s") ' % (product_code, product_name, comment_content, comment_time))
            conn.commit()

        print('结束抓取第%d页的评论......................................' % (i + 1))
        time.sleep(1)

    print('结束抓取 %s 下的评论..............................................' % tag_item[t][2])
    time.sleep(5)


cs.close()
conn.close()
