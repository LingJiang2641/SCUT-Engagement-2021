
import time
from selenium import webdriver
import pandas as pd


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


#改
browser.get('https://shopsearch.taobao.com/browse/shop_search.htm?q=%E6%9C%8D%E8%A3%85&imgfile=&commend=all&ssid=s5-e&search_type=shop&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=credit-desc&isb=0&shop_type=&ratesum=&s=1400')

#进入首页
browser.maximize_window()

input("登录")
print("登录成功")
time.sleep(1)

lst=[]

try:
    for i in range(71,101):
        for j in range(1,4):
            try:
                a=browser.find_element_by_xpath('//*[@id="list-container"]/li['+str(j)+']/ul/li[2]/h4/a[1]').text
                b=browser.find_element_by_xpath('//*[@id="list-container"]/li['+str(j)+']/ul/li[2]/h4/a[1]').get_attribute('trace-uid')
                c=browser.find_element_by_xpath('//*[@id="list-container"]/li['+str(j)+']/ul/li[2]/div/div[1]').text
                d = []
                for k in range(1,len(browser.find_elements_by_xpath('//*[@id="list-container"]/li['+str(j)+']/ul/li[2]/div/span/a'))+1):
                    d.append(browser.find_element_by_xpath('//*[@id="list-container"]/li['+str(j)+']/ul/li[2]/div/span/a['+str(k)+']').get_attribute('title'))
                e=browser.find_element_by_xpath('//*[@id="list-container"]/li['+str(j)+']/ul/li[2]/h4/a[1]').get_attribute('href')
                lst.append({'店铺名称':a,
                            '店铺id':b,
                            '好评率':c,
                            '承诺':d,
                            '网址':e})
                print('爬取成功')
            except:
                print('爬取失败')
                pass
            print('i='+str(i)+',j='+str(j))
        browser.execute_script("var q=document.documentElement.scrollTop=10000")
        if (i%5 == 0):
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
        browser.get('https://shopsearch.taobao.com/browse/shop_search.htm?q=%E6%9C%8D%E8%A3%85&imgfile=&commend=all&ssid=s5-e&search_type=shop&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=credit-desc&isb=0&shop_type=&ratesum=&s='+str(i*20))
        time.sleep(10)
    print("退出成功")
except :
    pass
    print("失败退出")
pd.DataFrame(lst).to_excel('店铺列表3.xlsx')


