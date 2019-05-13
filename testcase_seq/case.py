# coding=utf-8
'''定义各种测试用例'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


def dologin(driver, user, psw): # 登录，参数是用户名和密码  T3
    driver.find_element_by_name("username").clear()
    driver.find_element_by_name("username").send_keys(user)
    # element is hidden ,must execute js to obtain
    # driver.execute_script("document.getElementById('input-login-password').style.display='block';")
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(psw)
    driver.find_element_by_xpath("html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/form/table/tbody/tr[3]/td[2]/input").click()


def doquit(driver):  # 退出火狐
    driver.close()


def click_user(driver):  # T4
    xpath_click_event(driver, "html/body/table[2]/tbody/tr[2]/td[1]/form/a[5]")


def click_add_user(driver):  # T5
    driver.find_element_by_css_selector("input[type=\"button\"]").click()


def add_user(driver, usern, psw, pswt, utype):  # T7
    driver.find_element_by_name("username").send_keys(usern)
    driver.find_element_by_name("password").send_keys(psw)
    driver.find_element_by_name("password2").send_keys(pswt)
    if utype == "Admin":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Admin")
    elif utype == "Teacher":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Teacher")
    elif utype =="Substitute":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Substitute")
    elif utype == "Student":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Student")
    elif utype == "Parent":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Parent")
    driver.find_element_by_css_selector("input[type=\"button\"]").click()


def click_edit_user(driver):  # T10 勾选一个对象点击edit
    driver.find_element_by_css_selector("tr.even > td > input[name=\"delete[]\"]").click()
    driver.find_element_by_xpath("//input[@value='Edit']").click()


def edit_user(driver, username, epsw, epswt, etype): # T12 编辑用户
    driver.find_element_by_name("username").clear()
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(epsw)
    driver.find_element_by_name("password2").clear()
    driver.find_element_by_name("password2").send_keys(epswt)
    if etype == "Admin":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Admin")
    elif etype == "Teacher":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Teacher")
    elif etype == "Substitute":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Substitute")
    elif etype == "Student":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Student")
    elif etype == "Parent":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Parent")
    driver.find_element_by_css_selector("input[type=\"button\"]").click()


def edit_user2(driver, epsw, epswt, etype): # T12 编辑用户
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(epsw)
    driver.find_element_by_name("password2").clear()
    driver.find_element_by_name("password2").send_keys(epswt)
    if etype == "Admin":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Admin")
    elif etype == "Teacher":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Teacher")
    elif etype == "Substitute":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Substitute")
    elif etype == "Student":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Student")
    elif etype == "Parent":
        Select(driver.find_element_by_name("type")).select_by_visible_text("Parent")
    driver.find_element_by_css_selector("input[type=\"button\"]").click()


def is_element_exist(driver):
    try:
        # driver.find_element_by_id("htext")
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'htext')))
        driver.execute_script("document.getElementById('htext')")
        return False
    except:
        return True

def is_element_exist_sql(driver):
    try:
        # driver.find_element_by_id("eero")
        # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'eero')))
        driver.execute_script("document.getElementById('eero')")
        return False
    except:
        return True



def click_confirm(driver):  # T13
    alert = driver.switch_to_alert()
    alert.accept()


def delete_user(driver):  # T17 勾选一个对象删除
    driver.find_element_by_xpath("html/body/table[2]/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr/td/form/table/tbody/tr[14]/td[1]/input").click()
    driver.find_element_by_xpath("//input[@value='Delete']").click()
    alert = driver.switch_to_alert()
    alert.accept()

def id_click_event(driver, ids):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ids)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ids))).click()


def xpath_click_event(driver, xpath):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def css_click_event(driver, css):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()


def name_click_event(driver, name):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, name)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name))).click()


def class_click_event(driver, class_name):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name))).click()


def tag_click_event(driver, tag_name):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, tag_name))).click()


def link_click_event(driver, text):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, text)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, text))).click()


def handlenew(driver):
    # driver.switch_to_window(driver.window_handles[1])
    for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
        driver.switch_to_window(handle)


def input_value_by_id(driver, inid, invalue):
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, inid))).clear()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, inid))).send_keys(invalue)

def is_alterpresent(driver):
    driver.switch_to_alert()
    # EC.alert_is_present()(driver)


def click_event_xpath(driver, click_object):
    driver.find_element_by_xpath(click_object).click()


def click_event_input_one(driver,p1,v1,click_object):
    driver.find_element_by_name(p1).clear()
    driver.find_element_by_name(p1).send_keys(v1)
    driver.find_element_by_xpath(click_object).click()


def click_event_input_two(driver,p1,p2,v1,v2,click_object):
    driver.find_element_by_name(p1).clear()
    driver.find_element_by_name(p1).send_keys(v1)
    driver.find_element_by_name(p2).clear()
    driver.find_element_by_name(p2).send_keys(v2)
    driver.find_element_by_xpath(click_object).click()


def click_event_input_three(driver,p1,p2,p3,v1,v2,v3,click_object):
    driver.find_element_by_name(p1).clear()
    driver.find_element_by_name(p1).send_keys(v1)
    driver.find_element_by_name(p2).clear()
    driver.find_element_by_name(p2).send_keys(v2)
    driver.find_element_by_name(p3).clear()
    driver.find_element_by_name(p3).send_keys(v3)
    driver.find_element_by_xpath(click_object).click()


def click_event_input_four(driver,p1,p2,p3,p4,v1,v2,v3,v4,click_object):
    driver.find_element_by_name(p1).clear()
    driver.find_element_by_name(p1).send_keys(v1)
    driver.find_element_by_name(p2).clear()
    driver.find_element_by_name(p2).send_keys(v2)
    driver.find_element_by_name(p3).clear()
    driver.find_element_by_name(p3).send_keys(v3)
    driver.find_element_by_name(p4).clear()
    driver.find_element_by_name(p4).send_keys(v4)
    driver.find_element_by_xpath(click_object).click()





