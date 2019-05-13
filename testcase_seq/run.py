# coding=utf-8
import unittest
import case
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)
        # binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
        binary = FirefoxBinary("D:\\software\\firefox\\firefox.exe")
        # 这里要指定火狐的位置，因为它不是默认位置，默认的是在C:\\Program Files（x86）\\Mozilla Firefox\\firefox.exe
        driver = webdriver.Firefox(firefox_binary=binary)
        driver.implicitly_wait(30)
        driver.get("http://localhost/schoolmate/")

    def run(self):
        driver = self.driver
        # 执行封装的函数
        case.dologin(driver, u"test", u"test")  # T3
        # case.click_user(driver)  # T4
        # case.click_add_user(driver)   # T5
        # case.add_user(driver, u"java", u"java123", u"java123", u"Student") # T7
        # case.click_edit_user(driver)  # T10
        # case.edit_user(driver,u"javac", u"123", u"124")  # T12
        # case.edit_user(driver, u"javac", u"123", u"123")  # T14 edit成功，各参数不为空且psw =psw2
        # case.click_confirm(driver)  # T13  有问题
        case.doquit(driver)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()
