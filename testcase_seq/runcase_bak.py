# coding=utf-8
import case
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib2
import EFSM_handle

'''调用封装好的各种测试用例'''


def runtestcase(unvardata, invidual):
    startTime = datetime.now()
    binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
    # 这里要指定火狐的位置，因为它不是默认位置，默认的是在C:\\Program Files（x86）\\Mozilla Firefox\\firefox.exe
    driver = webdriver.Firefox(firefox_binary=binary)
    # driver.implicitly_wait(30)
    driver.get("http://localhost/schoolmate2/")
    # 执行封装的函数
    case.dologin(driver, u"test", u"1")  # T3
    case.click_user(driver)  # T4
    case.click_add_user(driver)  # T5
    if invidual[1] != invidual[2]:
        case.add_user(driver, invidual[0], invidual[1], invidual[2], invidual[3])  # T7 添加用户得考虑用户已存在
        case.click_confirm(driver)  # T13
        case.doquit(driver)
        endtime = datetime.now()
        print "执行测试用例用时：", endtime - startTime
    else:
        case.add_user(driver, invidual[0], invidual[1], invidual[2], invidual[3])  # T7 添加用户得考虑用户已存在
        # case.delete_user(driver)
        # driver.implicitly_wait(10)
        flag = case.is_element_exist(driver)
        flag2 = case.is_element_exist_sql(driver)
        if flag2 == False:  # 先判断是否有因为输入特殊字符导致SQL语法错误，有就退出
            case.doquit(driver)
        else:  # 没有SQL语法错误继续往下判断
            if flag == False:  # 判断存在不存在用户名重复，重复则点击back，退出浏览器
                driver.find_element_by_id("back").click()
                case.doquit(driver)
            else:  # 不存在该元素，即用户名没有重复，往下运行
                case.click_edit_user(driver)  # T10
                # case.edit_user2(driver, unvardata[3], unvardata[4], unvardata[8])  # T12edit不成功
                # case.click_confirm(driver)  # T13
                case.edit_user2(driver, unvardata[6], unvardata[7], unvardata[9])  # T14 edit成功，各参数不为空且psw =psw2
                case.click_confirm(driver)  # T13
                # case.delete_user(driver)
                case.doquit(driver)

        endtime = datetime.now()
        print "执行测试用例用时：", endtime - startTime


def te():
    driver = webdriver.Remote("https://localhost:4444/wd/hub",
                              desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
    driver.get('http://www.baidu.com')
    el = driver.find_element_by_id('su')
    print el.get_attribute('value')
    driver.quit()


def seq_script(tevent):
    print "a", tevent


if __name__ == '__main__':
    # u = [1,2,3,4,5,6,"1","1",8,"Parent"]
    # t=["132","1","2","Student"]
    # runtestcase(u,t)
    # te()
    binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
    # 这里要指定火狐的位置，因为它不是默认位置，默认的是在C:\\Program Files（x86）\\Mozilla Firefox\\firefox.exe
    driver = webdriver.Firefox(firefox_binary=binary)
    # driver.implicitly_wait(30)
    driver.get("http://localhost/schoolmate2/")
    # 执行封装的函数
    case.dologin(driver, u"test", u"test")  # T3
    case.click_user(driver)  # T4
    case.delete_user(driver)