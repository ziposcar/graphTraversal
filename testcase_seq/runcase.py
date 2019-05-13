# coding=utf-8
import case
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib2

import sys
sys.path.append("D:\\WandS\\Graduation_Project\\graphTraversal-submit")
import EFSM_handle

import re
'''调用封装好的各种测试用例'''

def runtestcase(unvardata, invidual):
   startTime = datetime.now()
   binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
   # 这里要指定火狐的位置，因为它不是默认位置，默认的是在C:\\Program Files（x86）\\Mozilla Firefox\\firefox.exe
   driver = webdriver.Firefox(firefox_binary = binary)
   # driver.implicitly_wait(30)
   driver.get("http://localhost/schoolmate2/")
   #执行封装的函数
   case.dologin(driver, u"test", u"1")  # T3
   case.click_user(driver)  # T4
   case.click_add_user(driver)   # T5
   if invidual[1] != invidual[2]:
       case.add_user(driver, invidual[0], invidual[1], invidual[2], invidual[3]) # T7 添加用户得考虑用户已存在
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
       if flag2 == False: # 先判断是否有因为输入特殊字符导致SQL语法错误，有就退出
           case.doquit(driver)
       else: # 没有SQL语法错误继续往下判断
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
    driver = webdriver.Remote("https://localhost:4444/wd/hub",desired_capabilities= webdriver.DesiredCapabilities.HTMLUNIT)
    driver.get('http://www.baidu.com')
    el = driver.find_element_by_id('su')
    print el.get_attribute('value')
    driver.quit()


# 脚本库自动产生
#3个参数：tevent所有迁移的event信息，pathT 当前迁移序列,针对变量产生的数据
def seq_script(driver,tevent,pathT,induval):
    infor = []
    for T in pathT:
        infor.append(tevent[T])
    # print "pathT\n",pathT
    # print "infor\n",infor
    # print "tevent\n", tevent
    j = 0
    for T_info in infor:
        T_info = T_info.split(";")
        print T_info, "\n"
        if T_info[0] =="" and T_info[2] == "click":
            # 属于没有输入变量的click事件,call click()
            temp = T_info[1].split("=")
            if temp[0] == "xpath": # 对象类型
                case.click_event_xpath(driver, temp[1])
            elif temp[0] == "css":
                print "后续补"
        elif T_info[0] != "" and T_info[2] == "click":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 1:  #最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                case.click_event_input_one(driver,t[0],induval[j-1],temp[1])
            elif temp[0] == "xpath" and len(t) == 2:
                case.click_event_input_two(driver,t[0],t[1],induval[j-2],induval[j-1],temp[1])
            elif temp[0] == "xpath" and len(t) == 3:
                case.click_event_input_three(driver, t[0], t[1],t[2],induval[j - 3], induval[j - 2], induval[j - 1], temp[1])
            elif temp[0] == "xpath" and len(t) == 43:
                case.click_event_input_four(driver, t[0], t[1], t[2],t[3],induval[j - 4], induval[j - 3], induval[j - 2], induval[j - 1],
                                             temp[1])
                print "后续补"
        elif T_info[0] != "" and T_info[2] == "事件类型补充":
            print "后续补充扩展"
    case.doquit(driver)



if __name__ == '__main__':
    # u = [1,2,3,4,5,6,"1","1",8,"Parent"]
    # t=["132","1","2","Student"]
    # runtestcase(u,t)
    # te()

    binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
    # # 这里要指定火狐的位置，因为它不是默认位置，默认的是在C:\\Program Files（x86）\\Mozilla Firefox\\firefox.exe
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.implicitly_wait(30)
    driver.get("http://localhost/schoolmate-a/")
    # 执行封装的函数
    # case.dologin(driver, u"test", u"test")  # T3
    # case.click_user(driver)  # T4
    # case.delete_user(driver)
    # driver = 1
    pathT=['T3', 'T101', 'T102', 'T104']
    tevent = "模型的迁移序列集"
    # print tevent
    induval = ['test','1',"abll",'ablfc']  #个体变量的数据，产生关于用户名密码的统统人为化，一遍得以进入系统
    seq_script(driver,tevent,pathT,induval)