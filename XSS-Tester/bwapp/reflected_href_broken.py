from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
from html import unescape
from html import escape

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

def init_bwapp():
    # open Chrome and go to bwapp
    url = "http://localhost/bWAPP/login.php"
    driver.get(url)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(3)

    # find login elements
    login = driver.find_element_by_xpath('//*[@id="login"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    submit = driver.find_element_by_xpath('//*[@id="main"]/form/button')

    login.send_keys('bee')
    password.send_keys('bug')
    submit.click()

    # reflected-get page
    url_og = 'http://localhost/bWAPP/xss_href-2.php?name=INPUT&action=vote'
    driver.get(url_og)


if __name__ == '__main__':

    #load in data from file
    input_arr = []
    file = open('input.txt', 'r')

    for line in file:
        input_arr.append(line.strip())

    init_bwapp()
    success = 0
    time.sleep(5)

    for input in input_arr:
        try:
            print('here')
            url = 'http://localhost/bWAPP/xss_href-2.php?name=>' + input + '<&action=vote'
            driver.get(url)
            time.sleep(1)
        except UnexpectedAlertPresentException:
            success += 1
            driver.execute_script('window.alert = null')
            init_bwapp()
            print('cleared')

    score = (success/len(input_arr)) * 100
    print('success:', str(success), ' out of', str(len(input_arr)))
    print('score:', str(score), '%')

