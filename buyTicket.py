from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import winsound
import time

#12306登录
def login(us,pw):
    driver.get("https://kyfw.12306.cn/otn/resources/login.html")#打开网址
    driver.find_element_by_xpath('//a[text()="账号登录"]').click()
    time.sleep(0.1)
    username= driver.find_element_by_xpath('//*[@id="J-userName"]')#获取用户名的位置
    password=driver.find_element_by_xpath('//*[@id="J-password"]')#获取密码的位置z
    username.send_keys(us)#输入用户名
    password.send_keys(pw)#输入密码
    while True:
        #链接跳转则，登录成功
        if driver.current_url=='https://kyfw.12306.cn/otn/view/index.html':
            break

#12306查询
def query():
    driver.get('https://kyfw.12306.cn/otn/leftTicket/init')#打开网址
    fromStationText=driver.find_element_by_xpath('//*[@id="fromStationText"]')#获取出发点的位置
    toStationText=driver.find_element_by_xpath('//*[@id="toStationText"]')#获取目的地的位置
    #要先点击一下，在清楚输入框的内容，再输入内容，再按键盘Down键，最后再按tab键
    fromStationText.click()
    fromStationText.clear()
    fromStationText.send_keys(fromStation)
    fromStationText.send_keys(Keys.DOWN)
    fromStationText.send_keys(Keys.TAB)
    toStationText.click()
    toStationText.clear()
    toStationText.send_keys(toStation)
    toStationText.send_keys(Keys.DOWN)
    toStationText.send_keys(Keys.TAB)
    #用js输入时间
    js="document.getElementById('train_date').value='%s'"%date
    driver.execute_script(js)
    time.sleep(1)#等待1s

    while True:
        xpath='//*[@id="query_ticket"]'
        if XpathExist(driver,xpath):
            try:
                driver.find_element_by_xpath(xpath).click()#点击查询按钮
                print("查询中...")
                break
            except:
                continue

#抢票
def XpathExist(driver,xpath):
      """
      检查xpath是否存在
      :param driver,xpath:
      :return:
      """
      try:
            driver.find_element_by_xpath(xpath)#若不存在会抛出异常
            return True
      except:
            return False

def buyTicket():
    xpaths = []
    for number in numbers:
        xpaths.append("//a[text()='%s']/../../../../../td[13]/a"%number)
    while True:
        try:
            if driver.current_url=='https://kyfw.12306.cn/otn/confirmPassenger/initDc':
                    break
            for x in xpaths:
                if XpathExist(driver,x):
                    te=driver.find_element_by_xpath(x[:-5] + '4]')#获取座位类型元素
                    tm=driver.find_element_by_xpath(x[:-5] + '3]')#获取座位类型元素
                    #判断所选座位是否有票
                    if tm.text=='有' or int(tm.text)>0 or te.text=='有' or int(te.text)>0:
                        order=driver.find_element_by_xpath(x)
                        order.click()
                        print("抢票中...")
                else:
                    xpath='//*[@id="query_ticket"]'
                    if XpathExist(driver,xpath):
                        try:
                            driver.find_element_by_xpath(xpath).click()
                        except:
                            print("重新点击")
        except:
           continue

#确认购票
def confirm():
    while True:
        try:
            xpath='//*[@id="content_defaultwarningAlert_hearder"]/a'
            if XpathExist(driver,xpath):
                driver.find_element_by_xpath(xpath)
                print(driver.find_element_by_xpath(xpath))
            else:
                xpaths=[]
                for passenger in passengers:
                    xpaths.append('//label[text()="%s"]'%passenger)
                while True:
                    try:
                        # sel = driver.find_element_by_id('seatType_1')
                        # Select(sel).select_by_value('O')#选取座位为二等座
                        for xpath in xpaths:
                            driver.find_element_by_xpath(xpath).click()#添加购票人
                        break
                    except:
                        continue
                # time.sleep(30000)
                xpath='//*[@id="dialog_xsertcj_ok"]'
                if XpathExist(driver,xpath):
                    print("确认弹出窗口中...")
                    while True:
                        try:
                            driver.find_element_by_xpath(xpath).click()
                            break
                        except:
                            break
                xpath='//*[@id="content_defaultwarningAlert_title"]'
                if XpathExist(driver,xpath):
                     print('目前没票')
                else:
                    print("点击成功")
                    driver.find_element_by_xpath('//*[@id="submitOrder_id"]').click()
                    while True:
                        try:
                            if driver.current_url!='https://kyfw.12306.cn/otn/confirmPassenger/initDc':
                                print("抢票成功，请及时付款")
                                break
                            xpath='//*[@id="orderResultInfo_id"]/div/span'
                            if XpathExist(driver,xpath):
                                print('抢票失败')
                                break
                            driver.find_element_by_xpath('//*[@id="qr_submit_id"]').click()

                        except:
                            continue
                    break
        except:
            continue

fromStation='汉口'
toStation='利川'
date='2019-01-31'
numbers=['D7063','D629','D2373','D5752','D2259','D353','D2255',
         'D637','D2237','D2207','D361','D2223','G1313','D2243','D5997']
passengers=['姓名1','姓名2']
driver=webdriver.Chrome()#加载chrome驱动

login('账号','密码')#登录
query()#查询
buyTicket()#抢票
print('qiangpiao')
confirm()#购票
winsound.Beep(400,100000)
