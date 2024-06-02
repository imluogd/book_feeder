import requests
from bs4 import BeautifulSoup
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time


def get_popular_book()->list[dict]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    # 目标URL
    #url = 'https://book.douban.com/'
    url = 'https://book.douban.com/chart?subcat=all'

    # 发送请求获取页面内容
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    book_contents = soup.find_all('div', class_='media__body')
    #pattern = re.compile(r'<a class="fleft" href="[^"]+">([^<]+)</a>.*?<p class="subject-abstract color-gray">\s*([^/]+)\s*/\s*([\d-]+)\s*/\s*([^/]+)\s*/', re.DOTALL)
    pattern = re.compile(r'<a class="fleft" href="([^"]+)">([^<]+)</a>.*?<p class="subject-abstract color-gray">\s*([^/]+)\s*/\s*([\d-]+)\s*/\s*([^/]+)\s*/', re.DOTALL)
    book_info = []
    for content in book_contents:
        match = pattern.search(str(content))
        if match:
            url = match.group(1)
            title = match.group(2)
            author = match.group(3).strip()
            date = match.group(4).strip()
            publisher = match.group(5).strip()
            book_info.append({'title': title.strip(), 'author': author.strip(), 'date':date.strip(),'publisher': publisher.strip(), 'url': url.strip()})
    return book_info
    # books=[]
    # for match in matches:
    #     book_info = {
    #         "title": match[0].strip(),
    #         "author": match[1].strip(),
    #         "date": match[2].strip(),
    #         "publisher": match[3].strip()
    #     }
    #     books.append(book_info)
    # return books
def get_new_books(num_pages:int=5)->list[dict]:
    url_0='https://book.douban.com/latest?p='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    book_info = []
    for i in range(num_pages):#爬取5页
        url=url_0+str(i+1)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        book_contents = soup.find_all('div', class_='media__body')
        pattern = re.compile(r'<a class="fleft" href="([^"]+)">([^<]+)</a>.*?<p class="subject-abstract color-gray">\s*([^/]+)\s*/\s*([\d-]+)\s*/\s*([^/]+)\s*/', re.DOTALL)
        for content in book_contents:
            match = pattern.search(str(content))
            if match:
                url = match.group(1)
                title = match.group(2)
                author = match.group(3).strip()
                date = match.group(4).strip()
                publisher = match.group(5).strip()
                book_info.append({'title': title.strip(), 'author': author.strip(), 'date':date.strip(),'publisher': publisher.strip(), 'url': url.strip()})
    return book_info   
def search_zlib(info:str):
    '''
    一般不注意格式，只需要书名（作者甚至也不需要，一般）'''
    book_title=info['title']
    book_author=info['author']
    #search_url='https://zh.zlibrary-global.se/s'+f'/?q={book_title}+{book_author}'
    search_url='https://zh.singlelogin.re/s'+f'/?q={book_title}+{book_author}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    response.encoding = 'utf-8'
    # 重要！！！
    # 假设zlib的搜索很靠谱，直接返回第一个搜索结果^_^
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_link = 'https://zh.zlibrary-global.se'+soup.find('a')['href']
    print(book_link)
    #需要模拟登录？但是从浏览器登出发现不需要登录也可以搜索，获取下载链接
def download_book(book_info:dict):
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    proxy = "http://127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)  
    browser = webdriver.Chrome(options=chrome_options)
    login_url = "https://zh.singlelogin.re/login.php"
    browser.get(login_url)
    browser.implicitly_wait(8)
    email_input = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/input')
    email_input.send_keys('1375472577@qq.com')
    password_input = browser.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys('luoguangda1')
    login_submit_button = browser.find_element(By.XPATH, '//button[@name="submit"]')
    login_submit_button.click()
    search_input = browser.find_element(By.ID, 'searchFieldx')
    query_content = f'{book_info["title"]} {book_info["author"]}'
    search_input.send_keys(query_content)
    search_input.send_keys(Keys.RETURN)
    h3_element = browser.find_element(By.XPATH, '//h3[@itemprop="name"]')
    h3_child_a = h3_element.find_element(By.TAG_NAME, 'a')
    book_detail_url= h3_child_a.get_attribute('href')
    browser.get(book_detail_url)
    download_button = browser.find_element(By.XPATH, '//a[@class="btn btn-primary addDownloadedBook"]')
    download_link = download_button.get_attribute('href')
    browser.get(download_link)
    time.sleep(10)#10 s在所有情况下都能下载完？
    browser.quit()

def listdir_sorted_by_mtime(directory):
    files = os.listdir(directory)
    files_with_mtime = [(f, os.path.getmtime(os.path.join(directory, f))) for f in files]
    sorted_files = sorted(files_with_mtime, key=lambda x: x[1], reverse=True)
    return [f[0] for f in sorted_files]

def download_book(book_list:list[dict]):
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    proxy = "http://127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)  
    browser = webdriver.Chrome(options=chrome_options)
    login_url = "https://zh.singlelogin.re/login.php"
    browser.get(login_url)
    browser.implicitly_wait(5)
    email_input = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/input')
    email_input.send_keys('1375472577@qq.com')
    password_input = browser.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys('luoguangda1')
    login_submit_button = browser.find_element(By.XPATH, '//button[@name="submit"]')
    login_submit_button.click()
    for book_info in book_list:
        search_input = browser.find_element(By.ID, 'searchFieldx')
        query_content = f'{book_info["title"]} {book_info["author"]}'
        search_input.send_keys(query_content)
        search_input.send_keys(Keys.RETURN)
        h3_element = browser.find_element(By.XPATH, '//h3[@itemprop="name"]')
        h3_child_a = h3_element.find_element(By.TAG_NAME, 'a')
        book_detail_url= h3_child_a.get_attribute('href')
        browser.get(book_detail_url)
        download_button = browser.find_element(By.XPATH, '//a[@class="btn btn-primary addDownloadedBook"]')
        download_link = download_button.get_attribute('href')
        browser.get(download_link)
        time.sleep(3)
        print(f"《{book_info['title']}》已经下载到{download_dir}/{listdir_sorted_by_mtime(download_dir)[0]}")
        browser.back()
        browser.back()
        search_input.clear()       
    browser.quit()
