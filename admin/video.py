import requests
import pymysql
import time
import random
import re
# 网页的请求头
header = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
}

if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "root", "gather_data")
    cursor = db.cursor()
    count = 152
    while count <= 402:

        select_sql = """SELECT page_url FROM li_video WHERE id = '%d'"""%int(count)
        cursor.execute(select_sql)
        urls = cursor.fetchone()
        random_time = random.randint(1, 5)
        time.sleep(random_time)
        print(random_time)

        for (url) in urls:
            exp = 'srcUrl="(.*?)",'
            detail_text = requests.get(url, headers=header).text
            video_url = re.findall(exp, detail_text, re.S)[0]
            print(video_url)
            update_sql="""UPDATE li_video SET video_url='%s' WHERE id='%d'"""%(str(video_url),int(count))
            cursor.execute(update_sql)
            db.commit()
            count = count+1

    db.close()