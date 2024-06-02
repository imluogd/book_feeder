import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
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
book_list=[{'title': '食南之徒', 'author': '马伯庸', 'date': '2024-4-1', 'publisher': '湖南文艺出版社', 'url': 'https://book.douban.com/subject/36710597/'}, {'title': '不理想的妻子', 'author': '王欣', 'date': '2024-4', 'publisher': '人民文学出版社', 'url': 'https://book.douban.com/subject/36866737/'}]
download_book(book_list)