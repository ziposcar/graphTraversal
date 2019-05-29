# coding=utf-8
import case
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib2
import re
import obtain_efsm_info2
import recordFun
import config
import time

options = webdriver.FirefoxOptions()
profile = webdriver.FirefoxProfile()
options.set_headless()
# options.add_argument('-headless')
# options.add_argument('--disable-gpu')
profile.set_preference("intl.accept_languages", "en-US");

binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
# # 这里要指定火狐的位置，因为它不是默认位置，默认的是在C:\\Program Files（x86）\\Mozilla Firefox\\firefox.exe
class Drivers(list):
    def __del__(self):
        for i in self:
            try:
                i.quit()
            except Exception as e:
                print e
                pass

drivers = Drivers()
multi_process_count = config.getPopParameter()[4]
for i in range(multi_process_count):
    driver = webdriver.Firefox(firefox_binary=binary, firefox_options=options, firefox_profile=profile)
    driver.implicitly_wait(30)
    drivers.append(driver)

# 脚本库自动产生
#3个参数：tevent所有迁移的event信息，pathT 当前迁移序列,针对变量产生的数据
def seq_script(driver,tevent,pathT,induval):
    infor = []
    # print "pathT\n", pathT
    # print "tevent\n", tevent
    for T in pathT:
        infor.append(tevent[T])
    # print "infor\n",infor
    j = 0
    # print "pathT",pathT
    # print "info",infor
    for info in range(len(infor)):
        # print "infor[info]",infor[info]
        T_info = infor[info]
        tt = pathT[info]
        print " 处理 %s 迁移" % tt
        T_info = T_info.split(";")
        # print T_info
        if T_info[0] =="" and T_info[2] == "click":
            # 属于没有输入变量的click事件,call click()
            temp = T_info[1].split("=")
            if temp[0] == "xpath": # 对象类型
                if tt == "T19":
                    case.T19(driver,temp[1])
                elif tt == "T24":
                    case.T24(driver,temp[1])
                else:
                    case.click_event_xpath(driver, temp[1])
            elif temp[0] == "css":
                case.click_event_css(driver,temp[1])
            elif temp[0] == "link text":
                if tt == "T23":  #t33
                    case.click_event_links(driver)
                    case.click_event_links(driver)
                else:
                    case.click_link(driver)
            elif temp[0] == "name":
                case.click_event_name(driver,temp[1])
            elif temp[0] == "id":
                case.click_event_id(driver,temp[1])
        elif T_info[0] != "" and T_info[2] == "click":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            # print "迁移上变量：",t
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 1:  #最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                case.click_event_input_one(driver,t[0],induval[j-1],temp[1])
            elif temp[0] == "xpath" and len(t) == 2:
                case.click_event_input_two(driver,t[0],t[1],induval[j-2],induval[j-1],temp[1])
            elif temp[0] == "xpath" and len(t) == 3:
                case.click_event_input_three(driver, t[0], t[1],t[2],induval[j - 3], induval[j - 2], induval[j - 1], temp[1])
            elif temp[0] == "xpath" and len(t) == 4:
                if tt == "T29" or tt == "T37": #T44, T52要求密码相同
                    case.click_event_input_four_add(driver, t[0], t[1], t[2], t[3], induval[j - 4], induval[j - 2],
                                                induval[j - 2], induval[j - 1],
                                                temp[1])
                elif tt == "T61" or tt == "T66":
                    case.click_event_input_four_parent(driver, t[0], t[1], t[2],t[3],induval[j - 4], induval[j - 3], induval[j - 2], induval[j - 1],
                                             temp[1])
                else:
                    case.click_event_input_four(driver, t[0], t[1], t[2],t[3],induval[j - 4], induval[j - 3], induval[j - 2], induval[j - 1],
                                             temp[1])
            elif temp[0] == "xpath" and len(t) == 5:
                case.click_event_input_five(driver, t[0], t[1], t[2], t[3],t[4],induval[j - 5], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],temp[1])
            elif temp[0] == "xpath" and len(t) == 6:
                case.click_event_input_six(driver, t[0], t[1], t[2], t[3], t[4],t[5],induval[j - 6], induval[j - 5], induval[j - 4],
                                            induval[j - 3],induval[j - 2], induval[j - 1], temp[1])
            elif temp[0] == "xpath" and len(t) == 7:
                case.click_event_input_sevent(driver,t[0], t[1], t[2], t[3], t[4],t[5],t[6],induval[j - 7],
                                              induval[j - 6], induval[j - 5], induval[j - 4],
                                            induval[j - 3],induval[j - 2], induval[j - 1], temp[1])
            elif temp[0] == "xpath" and len(t) == 12:
                case.click_event_input_12(driver,t[0], t[1], t[2], t[3], t[4],t[5],t[6],t[7], t[8], t[9], t[10], t[11],
                                          induval[j - 12],induval[j - 11],induval[j - 10],induval[j - 9],induval[j - 8],
                                          induval[j - 7],induval[j - 6], induval[j - 5], induval[j - 4],
                                            induval[j - 3],induval[j - 2], induval[j - 1], temp[1])
            # 后续补
        elif T_info[0] != "" and T_info[2] == "down_click": #事件类型，下拉列表
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            # print "迁移上变量：", t
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 2:  # 最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                case.down_click_two(driver, t[0],t[1],temp[1])
            elif temp[0] == "xpath" and len(t) == 3:  # 最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                case.down_click_three(driver, t[0],t[1],t[2],temp[1])

            # print "后续补充扩展"
    case.doquit(driver)


def seq_script_faqforg(driver,tevent,pathT,induval):
    infor = []
    # print "pathT\n", pathT
    # print "tevent\n"#, tevent
    for T in pathT:
        infor.append(tevent[T])
    # print "infor\n",infor
    j = 0
    # print "pathT",pathT
    # print "info",infor
    for info in range(len(infor)):
        # print "infor[info]",infor[info]
        T_info = infor[info]
        tt = pathT[info]
        # print " 处理 %s 迁移" % tt
        T_info = T_info.split(";")
        # print"T_info[0]", T_info[0]
        if T_info[0] =="" and T_info[2] == "click":
            # 属于没有输入变量的click事件,call click()
            temp = T_info[1].split("=")
            if temp[0] == "xpath": # 对象类型
                case.click_event_xpath(driver, temp[1])
            elif temp[0] == "css":
                case.click_event_css(driver,temp[1])
            elif temp[0] == "link":
                case.click_event_link_all(driver,temp[1])
            elif temp[0] == "name":
                case.click_event_name(driver,temp[1])
            elif temp[0] == "id":
                case.click_event_id(driver,temp[1])
        elif T_info[0] != "" and T_info[2] == "click":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            # print "迁移上变量：",t
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 1:  #最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                case.click_event_input_one(driver,t[0],induval[j-1],temp[1])
            elif temp[0] == "xpath" and len(t) == 4:
                case.click_event_input_four_faq(driver, t[0], t[1], t[2], t[3], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],
                                            temp[1])
            elif temp[0] == "xpath" and len(t) == 5:
                case.click_event_input_five_faq(driver, t[0], t[1], t[2], t[3],t[4],induval[j - 5], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],temp[1])
            elif temp[0] == "css" and len(t) == 5:
                case.click_event_input_css_five(driver, t[0], t[1], t[2], t[3],t[4],induval[j - 5], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],temp[1])
            elif temp[0] == "name" and len(t) == 2: #登录要指定
                case.faqfore_T2_T3(driver,t[0],t[1],"admin","admin",temp[1])
            elif temp[0] == "name" and len(t) == 4:
                case.click_event_input_name_four(driver, t[0], t[1], t[2], t[3], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],
                                            temp[1])
    case.doquit(driver)


def seq_script_webchess(driver,tevent,pathT,induval):
    infor = []
    # print "pathT\n", pathT
    # print "tevent\n", tevent
    for T in pathT:
        infor.append(tevent[T])
    # print "infor\n",infor
    j = 0
    w = 0
    aw = 0
    # print "pathT",pathT
    # print "info",infor
    try:
        for info in range(len(infor)):
            # print "infor[info]",infor[info]
            T_info = infor[info]
            tt = pathT[info]
            print " 处理 %s 迁移" % tt
            T_info = T_info.split(";")
            # print"T_info[0]", T_info[0]
            if T_info[0] =="" and T_info[2] == "click":
                # 属于没有输入变量的click事件,call click()
                temp = T_info[1].split("=")
                if temp[0] == "xpath": # 对象类型
                    case.click_event_xpath(driver, temp[1])
                    time.sleep(1)
                elif temp[0] == "css":
                    case.click_event_css(driver,temp[1])
                elif temp[0] == "link":
                    case.click_event_link_all(driver,temp[1])
                elif temp[0] == "name":
                    case.click_event_name(driver,temp[1])
                elif temp[0] == "id":
                    case.click_event_id(driver,temp[1])
            elif T_info[0] != "" and T_info[2] == "click":
                # 属于有输入变量的click事件,call click_event_input()
                t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
                t = t.split(",")
                # print "迁移上变量：",t
                j = j + len(t)
                temp = T_info[1].split("=")
                if temp[0] == "xpath" and len(t) == 1:  #最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                    w,aw = case.webchess_T18(driver,t[0],induval[j-1],temp[1])
                elif temp[0] == "xpath" and len(t) == 2:
                    if tt == "T19":
                         case.webchess_T19(driver,t[0],t[1],induval[j-2],induval[j-1],temp[1])
                    else:
                         case.click_event_input_two(driver,t[0],t[1],induval[j-2],induval[j-1],temp[1])
                elif temp[0] == "xpath" and len(t) == 4:
                    case.click_event_input_four_webchess(driver, t[0], t[1], t[2], t[3], induval[j - 4], induval[j - 3],
                                                induval[j - 2], induval[j - 1],
                                                temp[1])
                elif temp[0] == "xpath" and len(t) == 5:
                    if tt == "T17":
                        case.webchess_T17(driver, t[0], t[1], t[2], t[3],t[4],induval[j - 5], induval[j - 4], induval[j - 3],
                                                induval[j - 2], induval[j - 1],temp[1])
                    else:
                        case.click_event_input_five(driver, t[0], t[1], t[2], t[3],t[4],induval[j - 5], induval[j - 4], induval[j - 3],
                                                induval[j - 2], induval[j - 1],temp[1])
                        time.sleep(1)
                        case.click_event_links(driver)
                elif temp[0] == "name" and len(t) == 9:
                    if tt == "T3":
                        case.webchess_T3(driver, t[0], t[1], t[2], t[3],t[4],t[5],t[6],t[7],t[8],induval[j-9],
                                                induval[j-8],induval[j - 7],induval[j-6],induval[j - 5], induval[j - 4], induval[j - 3],
                                                induval[j - 2], induval[j - 1],temp[1])
                    else:
                        case.webchess_T4(driver, t[0], t[1], t[2], t[3],t[4],t[5],t[6],t[7],t[8],induval[j-9],
                                                induval[j-8],induval[j - 7],induval[j-6],induval[j - 5], induval[j - 4], induval[j - 3],
                                                induval[j - 2], induval[j - 1],temp[1])
                elif temp[0] == "name" and len(t) == 2:
                    if tt == "T21":
                        case.webchess_T21(driver, t[0], t[1], induval[j - 2], induval[j - 1], temp[1],w,aw)
                    else:
                        case.webchess_T1(driver, t[0], t[1], "test", "1", temp[1])
    except:
        pass
    case.doquit(driver)


def seq_script_teacher(driver,tevent,pathT,induval):
    infor = []
    # print "pathT\n", pathT
    # print "tevent\n", tevent
    for T in pathT:
        infor.append(tevent[T])
    # print "infor\n",infor
    j = 0
    w = 0
    aw = 0
    # print "pathT",pathT
    # print "info",infor
    for info in range(len(infor)):
        # print "infor[info]",infor[info]
        T_info = infor[info]
        tt = pathT[info]
        print " 处理 %s 迁移" % tt
        T_info = T_info.split(";")
        # print"T_info[0]", T_info[0]
        if T_info[0] =="" and T_info[2] == "click":
            # 属于没有输入变量的click事件,call click()
            temp = T_info[1].split("=")
            if temp[0] == "xpath": # 对象类型
                case.click_event_xpath(driver, temp[1])
            elif temp[0] == "css":
                case.click_event_css(driver,temp[1])
            elif temp[0] == "link":
                # case.click_event_link_all(driver,temp[1])
                case.click_link(driver)
            elif temp[0] == "name":
                case.click_event_name(driver,temp[1])
            elif temp[0] == "id":
                case.click_event_id(driver,temp[1])
        elif T_info[0] != "" and T_info[2] == "click":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            # print "迁移上变量：",t
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 1:  #最好click对象都是xpath的，看t的长度知道有几个参数，从而调用哪个脚本
                case.down_click_xpath_one(driver,t[0],temp[1])
            elif temp[0] == "name" and len(t) == 1:
                case.down_click_name_one(driver,t[0],temp[1])
            elif temp[0] == "xpath" and len(t) == 3:
                case.click_event_input_three(driver, t[0], t[1], t[2], induval[j - 3],induval[j - 2], induval[j - 1],temp[1])
            elif temp[0] == "xpath" and len(t) == 4:
                case.click_event_input_four_teacher(driver, t[0], t[1], t[2], t[3], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],
                                            temp[1])
            elif temp[0] == "xpath" and len(t) == 5:
                    case.click_event_input_five(driver, t[0], t[1], t[2], t[3],t[4],induval[j - 5], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],temp[1])

    case.doquit(driver)


def seq_script_addressbook(driver,tevent,pathT,induval):
    infor = []
    for T in pathT:
        infor.append(tevent[T])
    j = 0
    # print "pathT",pathT
    # print "info",infor
    for info in range(len(infor)):
        # print "infor[info]",infor[info]
        T_info = infor[info]
        tt = pathT[info]
        print " 处理 %s 迁移" % tt
        T_info = T_info.split(";")
        # print"T_info[0]", T_info[0]
        if T_info[0] =="" and T_info[2] == "click":
            temp = T_info[1].split("=")
            if temp[0] == "xpath": # 对象类型
                case.click_event_xpath(driver, temp[1])
            elif temp[0] == "css":
                case.click_event_css(driver,temp[1])
            elif temp[0] == "link":
                case.click_event_link_all(driver,temp[1])
            elif temp[0] == "name":
                case.click_event_name(driver,temp[1])
            elif temp[0] == "id":
                case.click_event_id(driver,temp[1])
        elif T_info[0] != "" and T_info[2] == "click":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 1:
                if tt == "T14":
                    case.click_name_one_input(driver,t[0],induval[j-1],temp[1])
                else:
                    case.click_event_input_one(driver,t[0],induval[j-1],temp[1])
            elif temp[0] == "name" and len(t) == 1:
                case.upaload(driver,t[0],temp[1])
            elif temp[0] == "name" and len(t) == 4:
                case.addressbook_four_input(driver, t[0], t[1], t[2], t[3], induval[j - 4], induval[j - 3],
                                            induval[j - 2], induval[j - 1],
                                            temp[1])
            elif temp[0] == "xpath" and len(t) == 26:
                    case.addressbook_Ninput(driver,t,induval,j,temp[1])
            elif temp[0] == "xpath" and len(t) == 25:
                    case.addressbook_Ninput(driver,t,induval,j,temp[1])

    case.doquit(driver)


def seq_script_phpcss(driver,tevent,pathT,induval):
    infor = []
    for T in pathT:
        infor.append(tevent[T])
    j = 0
    # print "pathT",pathT
    # print "info",infor
    for info in range(len(infor)):
        # print "infor[info]",infor[info]
        T_info = infor[info]
        tt = pathT[info]
        print " 处理 %s 迁移" % tt
        T_info = T_info.split(";")
        yy=["T74","T75","T76","T77","T78","T79","T80","T81","T82","T83","T84","T85","T86","T87","T88","T89","T90"]
        y2=["T15","T18","T21","T24","T27","T30","T32","T35","T38","T40","T44","T47","T49","T50","T57","T91"]
        if T_info[0] =="" and T_info[2] == "click":
            temp = T_info[1].split("=")
            if temp[0] == "xpath": # 对象类型
                if tt in yy:
                    driver.switch_to_frame("topFrame")
                    case.click_event_xpath(driver, temp[1])
                else:
                    driver.switch_to_frame("mainFrame")
                    case.click_event_xpath(driver, temp[1])
                    if tt not in y2:
                        alert = driver.switch_to_alert()
                        alert.accept()
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "link":
                driver.switch_to_frame("leftFrame")
                case.php_link(driver,temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "name":
                driver.switch_to_frame("mainFrame")
                case.click_event_name(driver,temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "id":
                driver.switch_to_frame("mainFrame")
                case.click_event_id(driver,temp[1])
                alert = driver.switch_to_alert()
                alert.accept()
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
        elif T_info[0] != "" and T_info[2] == "click":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "xpath" and len(t) == 1:
                driver.switch_to_frame("mainFrame")
                case.php_id_one(driver,t[0],induval[j-1],temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "xpath" and len(t) == 2:
                driver.switch_to_frame("mainFrame")
                if tt == "T92":
                    case.click_event_input_two(driver, t[0], t[1], induval[j - 2], induval[j - 2], temp[1])
                else:
                    case.click_event_input_two(driver,t[0],t[1],induval[j-2],induval[j-1],temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "xpath" and len(t) == 5:
                driver.switch_to_frame("mainFrame")
                case.click_event_input_five(driver, t[0], t[1], t[2], t[3], t[4], induval[j - 5], induval[j - 4],
                                            induval[j - 3],induval[j - 2], induval[j - 1], temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "name" and len(t) == 1:
                driver.switch_to_frame("mainFrame")
                case.php_name_one(driver,t[0],induval[j-1],temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "name" and len(t) == 2:
                driver.switch_to_frame("mainFrame")
                case.php_name_two(driver, t[0],t[1],induval[j-2],induval[j - 1], temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "name" and len(t) == 3:
                driver.switch_to_frame("mainFrame")
                if tt =="T61":
                    case.T61(driver)
                elif tt =="T55":  #密码相同
                    case.php_name_three(driver, t[0], t[1], t[2], induval[j - 3], induval[j - 2], induval[j - 2],
                                        temp[1])
                else:
                    case.php_name_three(driver,t[0],t[1],t[2],induval[j-3],induval[j-2],induval[j - 1], temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "name" and len(t) == 6:
                driver.switch_to_frame("mainFrame")
                case.php_name_six(driver,t[0],t[1],t[2],t[3],t[4],t[5],induval[j-6],
                                  induval[j-5],induval[j-4],induval[j-3],induval[j-2],induval[j - 1], temp[1])
                driver.switch_to.default_content()
                driver.implicitly_wait(10)
            elif temp[0] == "name" and len(t) == 8:
                driver.switch_to_frame("mainFrame")
                case.php_name_eight(driver,t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],induval[j-8],
                                    induval[j-7],induval[j-6],induval[j-5],induval[j-4],induval[j-3],induval[j-2],induval[j - 1], temp[1])
                driver.switch_to.default_content()
                # driver.implicitly_wait(10)
        elif T_info[0] != "" and T_info[2] == "upload":
            # 属于有输入变量的click事件,call click_event_input()
            t = re.findall('[^()]+', T_info[0])[1]  # 提取输入变量
            t = t.split(",")
            j = j + len(t)
            temp = T_info[1].split("=")
            if temp[0] == "name" and len(t) == 1:
                driver.switch_to_frame("mainFrame")
                if tt=="T62": #数据恢复
                    url = "E:\\pycharm\\graphTraversal\\support\\20180921_all.sql"
                    case.T62(driver)
                else:
                    url="E:\\pycharm\\graphTraversal\\support\\888.png" #上传
                case.php_upload(driver, t[0], url, temp[1])
                driver.switch_to.default_content()



    case.doquit(driver)


def runcase(driver_index, tevent, pathT, induval, t_index):
    # startTime = datetime.now()
    # 执行封装的函数
    driver = drivers[driver_index]
    url = config.getUrl().format(t_index)
    driver.get(url)
    ###################################
    # schoolmate程序需要确保是正确登录状态直接将个体所谓前两个参数设为test，1,使关于用户名密码的统统人为化，以便得以进入系统
    # case.dologin(driver, "test", "1")   #schoolmate程序的登录
    # seq_script(driver, tevent, pathT, induval)
    ###################################
    # schoolmate程序需要确保是正确登录状态直接将个体所谓前两个参数设为test，1,使关于用户名密码的统统人为化，以便得以进入系统
    # case.dologin(driver, "t", "1")   #schoolmate程序的teacher身份登录
    # seq_script_teacher(driver, tevent, pathT, induval)
    ###################################
    # faqforg程序不需要登录
    # seq_script_faqforg(driver,tevent,pathT,induval)
    ###################################
    ###################################
    # webchess程序
    # seq_script_webchess(driver,tevent,pathT,induval)
    ###################################
    ###################################
    # addressbook程序需要登录
    # case.login(driver, "admin", "123")
    # seq_script_addressbook(driver,tevent,pathT,induval)
    ###################################
    # phpcss程序需要登录
    case.loginForPhpCss(driver, "admin", "admin")
    seq_script_phpcss(driver, tevent, pathT, induval)
    ###################################
    # endTime = datetime.now()
    # usertime = endTime - startTime
    # print 'endTime - startTime运行该测试用例用时:\t', endTime - startTime
    # recordFun.recordTestCaseRunTime(usertime)



if __name__ == '__main__':
    SM = obtain_efsm_info2.obtain_efsm()  #注意对应的模型是哪个
    print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    # pathT = ['T3', 'T101', 'T102', 'T104']
    # pathT = ['T19', 'T22', 'T23', 'T89', 'T30', 'T31', 'T30', 'T31', 'T90', 'T39', 'T40', 'T41', 'T42', 'T80']
    #  'T21','T20', 'T22'中的T20是人工加的，序列能否顺利执行，还取决与模型建的准不准确，状态完不完整
    # 还要注意是几个输入变量
    #  下拉列表的，不能用clear后填值
    # induval = ['ouh2RA', '37409t', '2qFVBC']
    # induval =  ['8tn8X6', '4Mz63Q']
    # pathT=['T1', 'T3', 'T6', 'T7', 'T11', 'T22', 'T4']
    # pathT = ['T1', 'T3', 'T6', 'T7', 'T8', 'T4']
    # induval = ['rB9m6O', '0RW02i', '7t58M4', 'bDxdsI', 'qYky7B', 'w00h1a']
    # pathT = ['T1', 'T3', 'T8', 'T8', 'T9', 'T10', 'T4']
    # induval = ['kl3HqN', 'sLu3a8', 'uZRQq7', 'luVSf9', '8eM4Uk', 'tRQaRi', 'S3lp4u', 'mEhAd9', 'c50tyY', 'Nt5Fe3']
    # pathT=['T1', 'T3', 'T11', 'T13', 'T13', 'T22', 'T8', 'T8', 'T5', 'T6', 'T7', 'T6', 'T7', 'T4']
    # induval = ['5v0v38', '28q1kK', 'bLp2JW', '1744BZ', 'X1zsOX', 'Lym34F', 'HTYE4W', 'l53q4s', 'HpiO8K', 'SyC6UF']
    # pathT=['T1', 'T3', 'T11', 'T13', 'T13', 'T22', 'T8', 'T8', 'T5', 'T6', 'T7', 'T6', 'T7', 'T4']
    # induval =['5v0v38', '28q1kK', 'bLp2JW', '1744BZ', 'X1zsOX', 'Lym34F', 'HTYE4W', 'l53q4s', 'HpiO8K', 'SyC6UF']
    # pathT =['T1', 'T3', 'T5', 'T9', 'T10', 'T5', 'T11', 'T13', 'T12', 'T16', 'T20', 'T21', 'T22', 'T23', 'T4']
    # induval = ['ToYBC0', 'XgA5Sx', '7wyLft', 'Yjb6VD', '7O7W13', '2M3Sjm', 'D0Bn5N']
    # pathT = ['T1', 'T3', 'T8', 'T11', 'T14', 'T12', 'T16', 'T17', 'T12', 'T21', 'T7', 'T9', 'T10', 'T4']
    # induval = ['vfpLQw', '4r0qA7', 'k7Tx8s', 'HWbYHx', 'K83MZ4', 'RRn52o', 'KnZiTX', 'qAuo89', '907ngu', 'N8j00s', 'UjFCAd', 'EXG56V', '73us2Q', 'gja9uS', 'BW0Uvv', 'KSa6D5', '9dq993']
    # pathT = ['T56', 'T57', 'T58', 'T57', 'T58', 'T94', 'T60', 'T61', 'T64', 'T65', 'T66', 'T95', 'T85']
    # induval = ['7F5Qft', 'u3Ni5x', 'V7Lmj7', 'hMOwT7', 'OSXr1k', 'jJ0DWD', 'VNS8l1', 'YEdy6J', '2hcb9U', '0F4QEB', '4PnmSF', '58g0G4', 'W1DmLp', '35IaJf', 'ueP2Ub', 'p1rlxG']
    # pathT=['T54', 'T55', 'T55', 'T93', 'T57', 'T58', 'T83']
    # pathT = ['T19','T24','T25','T26']
    # induval = ['5Y86wC', '5t6NbB', '5b3483', '3Wo1qa', 'sdiW9n', 'tS9Gf5', 'B6XJzl']

    # #webchess
    # pathT = ['T2','T3', 'T8', 'T16',]
    # # induval = ['b8FX46', '6PXgve', 'TOKogIs', '0Qg6Nvm', 'zv5xgwd', '95gKbq9', '81gg2E3', 'puAjgeb', 'xFgNgWAl', 'hgJpC81', 'RGgphgTW', '8yLgBAu', '0jjkg1F', 'Hqg0b9n', 'x0P6g5p', 'JIHgK1E', 'b9gxTcT', 'mM7VgM8']
    # induval =['iMSWR5', 'V5S1aw', 'I1qfff9qr', '7DwE2O', '06gghl86', 'AKB0jq', '13YdAD', '0OXXT7', 3243, '2V84EL', 'qdW84Q', '95lgsssgg5s7', '875']

    # teacher
    # pathT =['T1', 'T2', 'T13', 'T24', 'T13', 'T24', 'T5', 'T9', 'T10', 'T12', 'T9', 'T10', 'T11', 'T23', 'T21', 'T22']
    # induval =['2Fu6c3', 'J8wdqH', '16I9K3', 'sjH1d3', '2018-02-07', '2018-05-16']
    pathT=['T2', 'T64', 'T27', 'T28', 'T29', 'T78']
    induval= ['fR34Gt', 'i4EpzK', 'ptJ296', 'AwIabz', '3PITWG']
    tevent = SM.TEvent
    runcase(tevent, pathT, induval)


