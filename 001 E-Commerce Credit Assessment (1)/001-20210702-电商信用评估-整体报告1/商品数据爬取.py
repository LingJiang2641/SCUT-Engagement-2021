import csv
import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# from IPython.core.interactiveshell import InteractiveShell  #执行该代码可以使得当前nb支持多输出
# InteractiveShell.ast_node_interactivity = "all"


browser = webdriver.Chrome()
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
                                Object.defineProperty(navigator, 'webdriver', {
                                  get: () => Chrome
                                })
                              """
})

url ='https://www.taobao.com/'

#设置全局变量来存储数据

browser.get(url)
browser.maximize_window()
browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'site-nav-user')))  # 加载

print("登录成功")
#进入商品总浏览页
urls = ['https://shop130809627.taobao.com/','https://shop122685716.taobao.com/','https://shop119570506.taobao.com/'] #店铺总url
ids = ['2639837995','2533553115','2498512100'] #店铺总id
for i in range(66):
    data_list = []
    # try:
    if i%3 == 0 & i != 0:
        browser.quit()
        time.sleep(80)
        browser = webdriver.Chrome()
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                                                    Object.defineProperty(navigator, 'webdriver', {
                                                      get: () => Chrome
                                                    })
                                                  """
        })
        script = "Object.defineProperty(navigator,'webdriver',{get: ()=>false,});"
        browser.execute_script(script)
        # 改
        browser.get(
            'https://shopsearch.taobao.com/browse/shop_search.htm?q=%E6%9C%8D%E8%A3%85&imgfile=&commend=all&ssid=s5-e&search_type=shop&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=credit-desc&isb=0&shop_type=&ratesum=')
        # 进入首页
        browser.maximize_window()
        input("登录")
        print("登录成功")
        time.sleep(2)
        browser.get(urls[i])
    else:
        browser.get(urls[i]) #进入店铺
    print("进入成功")
    # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="shop'+ids[i]+'"]/div/div/div/div/a')))  # 加载
    browser.find_elements_by_class_name('link')[0].click() #所有分类
    for j in range(1,4):
        dict = {}
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_ShopSearchResult"]/div/div[2]/div[2]/dl[1]/dd[1]/a')))
        browser.find_element_by_xpath('//*[@id="J_ShopSearchResult"]/div/div[2]/div[2]/dl[' + str(j+1) + ']/dd[1]/a').click() #进入商品
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div[2]/span')))
        # 包邮情况
        deliv = browser.find_element_by_xpath('/html/body/div[6]/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div[2]/span').text
        dict['deliv'] = deliv
        #30天内交易成功数
        trans = browser.find_element_by_xpath('//*[@id="J_Counter"]/div/div[2]/a').get_attribute('title')
        dict['trans'] = trans
        # 发货时间
        time = browser.find_element_by_xpath('//*[@id="J_ServiceMarkInfo"]').text
        dict['time'] = time
        # 商家承诺
        promises = browser.find_elements_by_xpath('//*[@id="J_tbExtra"]/dl[1]/dd/a')
        ls = []
        for k in range(1, len(promises) + 1):
            ls.append(browser.find_element_by_xpath('//*[@id="J_tbExtra"]/dl[1]/dd/a[' + str(k) + ']').text)
        dict['ls'] = ls
        # 单笔捐赠
        if '公益宝贝' in ls:
            per = browser.find_element_by_xpath('//*[@id="J_PublicWelfare"]/div/div[2]/p[1]/strong[2]').text
            dict['per'] = per
            # 一共多少笔
            amount = browser.find_element_by_xpath('//*[@id="J_PublicWelfare"]/div/div[2]/p[1]/strong[3]').text
            dict['amount'] = amount
        #支付手段
        #//*[@id="J_tbExtra"]/dl[2]/dd/a[1]/text()
        pay = browser.find_elements_by_xpath('//*[@id="J_tbExtra"]/dl[2]/dd/a')
        list = []
        for m in range(1, len(pay) + 1):
            list.append(browser.find_element_by_xpath('//*[@id="J_tbExtra"]/dl[2]/dd/a[' + str(m) + ']').text)
        dict['pay'] = list
        print(dict)
        data_list.append(dict)
        browser.back()
    pd.DataFrame(data_list).to_excel('dataAdd/'+id+'.csv')
    print('获取成功')
    print("i=" + str(i) )
    # except :
    #     print('获取失败')
    #     pd.DataFrame(data_list).to_excel('dataAdd/'+ id +'.csv')
    #     pass

    # WebDriverWait(browser, 20).until(EC.presence_of_element_located(
    #     (By.XPATH, '//*[@id="J_ShopSearchResult"]/div/div[2]/div[2]/dl[1]/dd[1]/a')))  # 加载


    # time.sleep(10)





