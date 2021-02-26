# selenium-driver.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from pathlib import Path
import random
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool


def account_fun():
    with open('accounts.txt') as f:
        account_list = f.readlines()
        new_accounts = []
        for acc in account_list:
            acc = acc.replace("\n", "")
            acc = acc.split(",")
            new_acc = []
            for i in acc:
                i = i.strip()
                new_acc.append(i)
            # print(new_acc)
            new_accounts.append(new_acc)
    random.shuffle(new_accounts)
    account_tuple = tuple(new_accounts)
    return account_tuple


def selenium_driver(account):
    driver_path = Path('chromedriver.exe').as_posix()
    cookies_file_path = 'cookies/' + account[0] + '.txt'
    cookies_path = Path(cookies_file_path).as_posix()
    options = Options()

    # options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    website = "https://www.facebook.com/"

    with open(cookies_path) as cookie_file:
        cookies = json.load(cookie_file)
    # for website in self.cookies_websites:
    driver.get(website)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    return driver


def is_fb_logged_in(driver):
    driver.get("https://facebook.com")
    if 'Facebook – log in or sign up' in driver.title:
        return False
    else:
        return True


def fb_login(driver, account):
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(account[0])

    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(account[1])

    login_box = driver.find_element_by_name('login')
    login_box.click()


# function to wait for random time
def random_wait(a=0, b=None):
    if b == None:
        time.sleep(a)
    else:
        time.sleep(random.randrange(a, b))


def scroll_down(driver, n):
    html = driver.find_element_by_tag_name('html')
    for i in range(n):
        html.send_keys(Keys.PAGE_DOWN)
        random_wait(3, 7)


# like posts
def like_post(driver):
    # "//*[contains(text(), 'My Button')]"
    # '//div[contains(text(), "{0}") and @class="inner"]'.format(text)
    like_post = driver.find_elements_by_xpath("//*[contains(text(), 'Like')]")
    print(len(like_post))
    for ele in like_post:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)


# add friend
def add_friend(driver):
    add_friend = driver.find_elements_by_xpath("//*[contains(text(), 'Add Friend')]")
    print(len(add_friend))
    for ele in add_friend[:3]:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)


# like pages
def like_page(driver):
    like_page_url = 'https://www.facebook.com/pages/?category=top&ref=bookmarks'
    driver.get(like_page_url)
    scroll_down(driver, 1)
    like_page = driver.find_elements_by_xpath("//*[contains(text(), 'Like')]")
    print(len(like_page))
    for ele in like_page[1:10]:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)


def main(account):
    driver = selenium_driver(account)
    if is_fb_logged_in(driver):
        print("Already logged in")
    else:
        print("Not logged in. Login")
        fb_login(driver, account)
    # activities to perform
    scroll_down(driver, 10)
    like_post(driver)
    add_friend(driver)
    like_page(driver)
    driver.quit()


def multiprocess(n, pool_list):
    # n is number of process to run
    with Pool(n) as p:
        print(p.map(main, pool_list))


if __name__ == '__main__':
    accounts = account_fun()

    # for acc in accounts:
    #     main(acc)

    multiprocess(2, accounts)