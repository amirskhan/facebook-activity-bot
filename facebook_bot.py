# selenium-driver.py
import json
from selenium import webdriver
from pathlib import Path
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class SeleniumDriver(object):
    def __init__(
        self,
        # chromedriver path
        driver_path = 'chromedriver.exe',
        # pickle file path to store cookies
        cookies_file_path = 'cookies/cookies.txt',
        # list of websites to reuse cookies with
        # cookies_websites=["https://facebook.com"]
        website = "https://facebook.com"

    ):
        self.driver_path = Path(driver_path).as_posix()
        self.cookies_file_path = Path(cookies_file_path).as_posix()
        # self.cookies_websites = cookies_websites
        self.website = website
        # chrome_options = webdriver.ChromeOptions()
        options = Options()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(
            executable_path=self.driver_path,
            options=options
        )
        try:
            # load cookies for given websites
#             cookies = pickle.load(open(self.cookies_file_path, "rb"))
            with open(self.cookies_file_path) as cookie_file:
                cookies = json.load(cookie_file)
            # for website in self.cookies_websites:
            self.driver.get(self.website)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        except Exception as e:
            # it'll fail for the first time, when cookie file is not present
            print(str(e))
            print("Error loading cookies")

    def save_cookies(self):
        # save cookies
        cookies = self.driver.get_cookies()
#         json.dump(cookies, open(self.cookies_file_path, "wb"))
        with open(self.cookies_file_path, 'w') as outfile:
            json.dump(cookies, outfile, indent=4)

    def close_all(self):
        # close all open tabs
        if len(self.driver.window_handles) < 1:
            return
        for window_handle in self.driver.window_handles[:]:
            self.driver.switch_to.window(window_handle)
            self.driver.close()

    def quit(self):
        self.save_cookies()
        self.close_all()
        self.driver.quit()


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


def is_fb_logged_in():
    driver.get("https://facebook.com")
    if 'Facebook – log in or sign up' in driver.title:
        return False
    else:
        return True


def fb_login(username, password):
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(username)

    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(password)

    login_box = driver.find_element_by_name('login')
    login_box.click()


# function to wait for random time
def random_wait(a=0, b=None):
    if b == None:
        time.sleep(a)
    else:
        time.sleep(random.randrange(a,b))


def scroll_down(n):
    html = driver.find_element_by_tag_name('html')
    for i in range(n):
        html.send_keys(Keys.PAGE_DOWN)
        random_wait(3, 7)


# like posts
def like_post():
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
def add_friend():
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
def like_page():
    like_page_url = 'https://www.facebook.com/pages/?category=top&ref=bookmarks'
    driver.get(like_page_url)
    scroll_down(1)
    like_page = driver.find_elements_by_xpath("//*[contains(text(), 'Like')]")
    print(len(like_page))
    for ele in like_page[1:10]:
        try:
            if random.choice(['yes', 'no']) == 'yes':
                ele.click()
        except Exception as e:
            print(e)
        random_wait(3, 7)


if __name__ == '__main__':
    # extract accounts from accounts file
    accounts = account_fun()
    for account in accounts:
        cookie_path = 'cookies/' + account[0] + '.txt'
        selenium_object = SeleniumDriver(cookies_file_path=cookie_path)
        driver = selenium_object.driver
        username = account[0]
        password = account[1]
        if is_fb_logged_in():
            print("Already logged in")
        else:
            print("Not logged in. Login")
            fb_login(username, password)
        scroll_down(10)
        like_post()
        add_friend()
        like_page()
        selenium_object.quit()