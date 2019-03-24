import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random

# 网页的请求头
header = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
}

def con_sql(sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "gather_data")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    # db.close()

def get_page(url):
    response = requests.get(url, headers=header)

    # 通过BeautifulSoup进行解析出每个房源详细列表并进行打印
    soup_idex = BeautifulSoup(response.text, 'html.parser')
    result_li = soup_idex.find_all('li', {'class': 'list-item'})

    # 进行循环遍历其中的房源详细列表
    for i in result_li:
        # 由于BeautifulSoup传入的必须为字符串，所以进行转换
        page_url = str(i)
        soup = BeautifulSoup(page_url, 'html.parser')
        # 由于通过class解析的为一个列表，所以只需要第一个参数
        # 详细页面的函数调用
        # get_page_detail(result_href.attrs['href'])

        # 标题和标题链接
        result_href = soup.find_all('a', {'class': 'houseListTitle'})[0]
        title1 = result_href.attrs['title']
        title_url = result_href.attrs['href']

        # 图片连接
        # result_item_img = soup.find_all('div', {'class': 'item-img'})[0]
        item_img = soup.select('.item-img img')[0]
        img_url = item_img.attrs['src']

        # 2室2厅 94m² 低层(共28层) 2010年建造 杨菓
        house_type = soup.select('.details-item span')[0].text.replace(' ','')

        area = soup.select('.details-item span')[1].text.replace(' ','')
        area1 = int(area.replace('m²',''))

        floor = soup.select('.details-item span')[2].text.replace(' ','')

        build_time = soup.select('.details-item span')[3].text.replace(' ','')
        build_time1 = build_time.replace('年建造','')

        linkman = soup.select('.details-item .brokername')[0].text.replace(' ','')
        linkman1 = linkman.replace('','')

        # 地址
        location = soup.find_all('span', {'class': 'comm-address'})[0].text.replace(' ','')

        # 总价，平均价
        total_price = soup.find_all('span', {'class': 'price-det'})[0].text.replace(' ','')
        total_price1 = int(float(total_price.replace('万','')))
        average_price = soup.find_all('span', {'class': 'unit-price'})[0].text.replace(' ','')
        average_price1 = int(average_price.replace('元/m²',''))

        # 备注
        remark = soup.select('.tags-bottom')[0].text.replace(' ','')

        # 标题打印
        print(title1)

        # SQL 插入语句
        sql = """INSERT INTO ajk_resold_house_info(title,
                 title_url, img_url, house_type, area, floor, build_time, linkman, region, location, total_price, average_price, remark)
                 VALUES ('%s', '%s', '%s', '%s', '%d', '%s', '%d', '%s', '%s', '%s', '%d', '%d', '%s')"""%(str(title1), str(title_url), str(img_url), str(house_type), int(area1), str(floor), int(build_time1), str(linkman1), str(''), str(location) ,int(total_price1), int(average_price1), str(remark) )
        # 传入sql
        con_sql(sql)


        # 进行下一页的爬取
        result_next_page = soup_idex.find_all('a', {'class': 'aNxt'})
        if len(result_next_page) != 0:
            # 延时模拟真实访问速度
            random_time = random.randint(1,6)
            time.sleep(random_time)
            print("延时多少秒？%d"%int(random_time))
            # 函数进行递归
            get_page(result_next_page[0].attrs['href'])
        else:
            print('没有下一页了')


# # 进行字符串中空格，换行，tab键的替换及删除字符串两边的空格删除
# def my_strip(s):
#     return str(s).replace(" ", "").replace("\n", "").replace("\t", "").strip()
# # 由于频繁进行BeautifulSoup的使用，封装一下，很鸡肋
# def my_Beautifulsoup(response):
#     return BeautifulSoup(str(response), 'html.parser')
#
#
#
# # 详细页面的爬取
# def get_page_detail(url):
#     response = requests.get(url, headers=header)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # 标题什么的一大堆，哈哈
#         result_title = soup.find_all('h3', {'class': 'long-title'})[0]
#         result_price = soup.find_all('span', {'class': 'light info-tag'})[0]
#         result_house_1 = soup.find_all('div', {'class': 'first-col detail-col'})
#         result_house_2 = soup.find_all('div', {'class': 'second-col detail-col'})
#         result_house_3 = soup.find_all('div', {'class': 'third-col detail-col'})
#         soup_1 = my_Beautifulsoup(result_house_1)
#         soup_2 = my_Beautifulsoup(result_house_2)
#         soup_3 = my_Beautifulsoup(result_house_3)
#         result_house_tar_1 = soup_1.find_all('dd')
#         result_house_tar_2 = soup_2.find_all('dd')
#         result_house_tar_3 = soup_3.find_all('dd')
#         '''
#         文博公寓，省实验中学，首付只需70万，大三房，诚心卖，价可谈 270万
#         宇泰文博公寓 金水－花园路－文博东路4号 2010年 普通住宅
#         3室2厅2卫 140平方米 南北 中层(共32层)
#         精装修 19285元/m² 81.00万
#         '''
#         print(my_strip(result_title.text), my_strip(result_price.text))
#         print(my_strip(result_house_tar_1[0].text),
#               my_strip(my_Beautifulsoup(result_house_tar_1[1]).find_all('p')[0].text),
#               my_strip(result_house_tar_1[2].text), my_strip(result_house_tar_1[3].text))
#         print(my_strip(result_house_tar_2[0].text), my_strip(result_house_tar_2[1].text),
#               my_strip(result_house_tar_2[2].text), my_strip(result_house_tar_2[3].text))
#         print(my_strip(result_house_tar_3[0].text), my_strip(result_house_tar_3[1].text),
#               my_strip(result_house_tar_3[2].text))

if __name__ == '__main__':
    # url链接
    url = 'https://xa.anjuke.com/sale/'
    get_page(url)