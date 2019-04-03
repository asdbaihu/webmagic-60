import requests
import pymysql
import time
import random
import re

# 网页的请求头
# header = {
#     # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
#     # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
#     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
# }

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Proxy-Connection': 'keep-alive',
    'Host': 'www.meituan.com',
    'Referer': 'http://xa.meituan.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type': 'text/html;charset=utf-8',
    'Cookie': '_lxsdk_cuid=169ab78c87014-01e42998804d2f-5d1f3b1c-1fa400-169ab78c8721b; _lxsdk=169ab78c87014-01e42998804d2f-5d1f3b1c-1fa400-169ab78c8721b; ci=42; _hc.v=50728862-e744-383d-88e2-a93bb608db47.1553360041; client-id=546f1af9-67d8-497f-ad0a-1a622e57126c; uuid=5947f655-fe3c-42d5-a889-aa9bac343ad6; lat=34.201751; lng=108.945737; _lxsdk_s=169e26c4691-b6d-0bf-324%7C%7C4',
}

if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "root", "gather_data")
    cursor = db.cursor()

    count = 1439
    while count <= 4418:
        select_sql = """SELECT shop_url FROM meituan_shop_info WHERE id = '%d'""" % int(count)
        cursor.execute(select_sql)
        urls = cursor.fetchone()
        random_time = random.randint(2, 8)
        time.sleep(random_time)
        print(random_time)

        for (url) in urls:
            exp = '"frontImgUrl":"(.*?)",'
            try:
                detail_text = requests.get(url, headers=header).text
                img_url = re.findall(exp, detail_text, re.S)[0]
            except:
                pass
            print(img_url)
            update_sql = """UPDATE meituan_shop_info SET img_url='%s' WHERE id='%d'""" % (str(img_url), int(count))
            cursor.execute(update_sql)
            db.commit()
            count = count + 1

    db.close()

