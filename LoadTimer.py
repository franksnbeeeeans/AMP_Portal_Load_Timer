from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from config import *


def site_login(username, password, driver, login_URL):
    driver.get(login_URL)
    driver.find_element_by_id("user_email").send_keys(username)
    driver.find_element_by_id("user_password").send_keys(password)
    driver.find_element_by_name("button").click()
    time.sleep(1)
    try:
        driver.find_element_by_xpath("//html/body/main/div/div[@class='flash-alert alert alert-danger alert-dismissible']")
        driver.quit()
        exit("Login failed, exiting.")
    except NoSuchElementException:
        pass


def timer(driver, source):
    driver.get(source)
    navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
    response_start = driver.execute_script("return window.performance.timing.responseStart")
    dom_complete = driver.execute_script("return window.performance.timing.domComplete")

    backend_performance = response_start - navigation_start
    frontend_performance = dom_complete - response_start
    time.sleep(3)
    driver.quit()

    print(f'\nCurrent time: {time.time()}')
    print(f'\nLoad times for {source}:')
    print(f'\nBack End: {backend_performance}ms')
    print(f'\nFront End: {frontend_performance}ms')
    print(f'\nTotal: {backend_performance+frontend_performance}ms')


def test_urls(username, password, login_URL, URLs):
    for URL in URLs:
        try:
            driver = webdriver.Chrome()
        except:
            exit("Download the appropriate version of chromedriver.exe for your Chrome version here:\n \
                  https://sites.google.com/a/chromium.org/chromedriver/downloads \n \
                  Place your chromedriver.exe in the directory with this script.")
        site_login(username, password, driver, login_URL)
        timer(driver, URL)
        driver.quit()


NAM_login_URL = "https://console.amp.cisco.com"
NAM_URLs = ['https://console.amp.cisco.com/dashboard',
        'https://console.amp.cisco.com/dashboard/events#/events/show/{}']

EU_login_URL = "https://console.eu.amp.cisco.com"
EU_URLs = ['https://console.eu.amp.cisco.com/dashboard',
        'https://console.eu.amp.cisco.com/dashboard/events#/events/show/{}']

APJC_login_URL = "https://console.apjc.amp.cisco.com"
APJC_URLs = ['https://console.apjc.amp.cisco.com/dashboard',
        'https://console.apjc.amp.cisco.com/dashboard/events#/events/show/{}']

test_urls(NAM_username, NAM_password, NAM_login_URL, NAM_URLs)
test_urls(EU_username, EU_password, EU_login_URL, EU_URLs)
test_urls(APJC_username, APJC_password, APJC_login_URL, APJC_URLs)

"""
Use Selenium to Measure Web Timing
Performance Timing Events flow
navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd
-> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd
-> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd
"""
