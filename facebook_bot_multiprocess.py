from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from pathlib import Path
import random
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
import psutil


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
    s = Service('chromedriver.exe')
    driver = webdriver.Chrome(
        service=s,
        options=options
    )
    website = "https://www.facebook.com/"
    try:
        with open(cookies_path) as cookie_file:
            cookies = json.load(cookie_file)
        # for website in self.cookies_websites:
        driver.get(website)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
    except Exception as e:
        # it'll fail for the first time, when cookie file is not present
        print("Cookies:", e)
    return driver


def is_fb_logged_in(driver):
    driver.get("https://facebook.com")
    if 'Facebook – log in or sign up' in driver.title:
        return False
    else:
        return True


def fb_login(driver, account):
    username_box = driver.find_element(By.ID, "email")
    username_box.send_keys(account[0])

    password_box = driver.find_element(By.ID, "pass")
    password_box.send_keys(account[1])

    login_box = driver.find_element(By.NAME, "login")
    login_box.click()


# function to wait for random time
def random_wait(a=0, b=None):
    if b == None:
        time.sleep(a)
    else:
        time.sleep(random.randrange(a, b))


def scroll_down(driver, n):
    #html = driver.find_elements(By.TAG_NAME, "html")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "html")))
    html = driver.find_element(By.TAG_NAME, "html")
    for i in range(n):
        html.send_keys(Keys.PAGE_DOWN)
        random_wait(3, 7)

# like posts
def like_post(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Like')]")))
    like_post = driver.find_elements(By.XPATH, "//*[contains(text(), 'Like')]")
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
    add_friend_url = 'https://www.facebook.com/friends/suggestions'
    driver.get(add_friend_url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add Friend')]")))
    add_friend = driver.find_elements(By.XPATH, "//*[contains(text(), 'Add Friend')]")
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
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Like')]")))
    like_page = driver.find_elements(By.XPATH, "//*[contains(text(), 'Like')]")
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
    with Pool(n) as p:
        print(p.map(main, pool_list))


if __name__ == '__main__':
    # extract accounts from accounts file
    accounts = account_fun()
    # number of process to run
    if len(accounts) >= 4:
        memory = int(str(psutil.virtual_memory().total)[0])
        if memory >= 8:
            n = 8
        else:
            n = 4
    else:
        n = len(accounts)

    multiprocess(n, accounts)
    
    
#https://texasvaluesaction.org/amirskhan/facebook-activity-bot
