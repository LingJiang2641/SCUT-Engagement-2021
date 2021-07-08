import csv
import time

import requests
from fake_useragent import UserAgent

id_lst=[#列表1
2209064897522,
2209501154582,
2209795029305,
2210228542894
]
ua = UserAgent().random
cookie='_dcc_session=dfqldg9qhr30s7psi7mbbrg7os; Hm_lvt_3a75bcb07225c9d03aae2d67edca6226=1624845895,1624860714,1624874935,1624875276; Hm_lvt_2dc49552d570922026e5fcb79894c7b3=1624845895,1624860714,1624874935,1624875276; acw_tc=781bad2016248769092844328e6a469a4d9038185ef7384feb735b3d435297; _sess_remember=27ee2b45b073d94323d40b1002655c77; Hm_lpvt_2dc49552d570922026e5fcb79894c7b3='+str(int(time.time()))+'; Hm_lpvt_3a75bcb07225c9d03aae2d67edca6226='+str(int(time.time()))

for id in id_lst:
    try:
        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-Encoding': 'gzip, deflate, br',
        'accept-Language': 'zh-CN,zh;q=0.9',
        'cache-Control': 'max-age=0',
        'connection': 'keep-alive',
        'cookie': cookie,
        'host': 'www.dianchacha.com',
        'Referer': 'https://www.dianchacha.com/shop/info/index/uid/'+str(id),
        'User-Agent': ua,
        }

        url4 = "https://www.dianchacha.com/shop/sales/reckonDo?k="+str(id)#销售额估算
        data_li = []
        dict4 = {}
        response4 = requests.get(url4,headers=headers).text
        print(response4)
        sel4 = response4.split('{')[2].split(':')[4:8]
        dict4['店铺id'] = id
        dict4['月销售额'] = sel4[0].split('"')[1]
        dict4['成交笔数'] = sel4[1].split('"')[1]
        dict4['平均客单价'] = sel4[2].split('"')[1]
        dict4['平均日销售额'] = sel4[3].split('"')[1]
        print(dict4)
        data_li.append(dict4)
        with open('salesForcast8.csv', 'a+', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_li[0].keys())  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
            writer.writeheader()  # 写入列名
            writer.writerows(data_li)
        print('第  '+str(id_lst.index(id))+'  的数据写入完成')
        time.sleep(20)
    except:
        print("失败退出")
        pass