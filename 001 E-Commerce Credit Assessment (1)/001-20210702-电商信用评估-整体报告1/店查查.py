import csv
import time

import requests
from parsel import Selector
from fake_useragent import UserAgent

ua = UserAgent().random

id_lst=[
387074871
]
cookie='acw_tc=76b20f7216248458936916972e503815453f004bc6dfeeb564a75ad2fb27a9; _dcc_session=n7cuhn5upu3lvdubvnbdve33lk; Hm_lvt_3a75bcb07225c9d03aae2d67edca6226=1624703637,1624760877,1624767287,1624845895; Hm_lvt_2dc49552d570922026e5fcb79894c7b3=1624703637,1624760877,1624767288,1624845895; _sess_remember=5cf18a2577d4010052ccc174d34827da; Hm_lpvt_2dc49552d570922026e5fcb79894c7b3='+str(int(time.time()))+'; Hm_lpvt_3a75bcb07225c9d03aae2d67edca6226='+str(int(time.time()))
print(cookie)
for id in id_lst:
    print(id_lst.index(id))
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-Encoding': 'gzip, deflate, br',
    'accept-Language': 'zh-CN,zh;q=0.9',
    'cache-Control': 'max-age=0',
    'connection': 'keep-alive',
    'cookie': cookie,
        'Referer': 'https://www.dianchacha.com/shop/info/index/uid/'+str(id),
    'User-Agent': ua,
    }

    data_list = []
    url3 = "https://www.dianchacha.com/shop/item/index/uid/"+str(id)+"/?orderBy=saleDESC&pageNum=1"#宝贝列表
    response3 = requests.get(url3, headers=headers).text
    print(response3)
    sel3 = Selector(response3)

    total_page = sel3.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/div/div/span/span[2]/text()').extract()[0]
    print(total_page)
    try:
        for i in range(int(total_page)):

            url = "https://www.dianchacha.com/shop/item/index/uid/"+str(id)+"/?orderBy=saleDESC&pageNum=" + str(i)  # 宝贝列表
            time.sleep(10)
            response = requests.get(url, headers=headers).text
            sel = Selector(response)
            for j in range(1,21):
                dict = {}  # 单个
                dict['序号']= sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[1]/text()').extract()[0]
                dict['宝贝名称']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[2]/a[2]/text()').extract()[0]
                dict['月销量']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[3]/text()').extract()[0]
                dict['评价数']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[4]/text()').extract()[0]
                dict['收藏数']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[5]/text()').extract()[0]
                dict['价格']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[6]/text()').extract()[0]
                dict['昨日销量']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[7]/text()').extract()[0]
                dict['昨日销售额']=sel.xpath('/html/body/div[2]/div[2]/div[3]/div[3]/table/tbody/tr['+str(j)+']/td[8]/text()').extract()[0]
                if dict['月销量'] == '0':
                    break
                data_list.append(dict)
            print("i = " + str(i))


        with open(str(id)+'.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_list[0].keys())  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
            writer.writeheader()  # 写入列名
            writer.writerows(data_list)
        print("成功退出")

    except:
        pass
        print("失败退出")
    print('csv文件写入完成')
    time.sleep(10)

