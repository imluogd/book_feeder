import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
proxy = "http://127.0.0.1:7890"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={proxy}')
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
browser.implicitly_wait(8)

search_input = browser.find_element(By.ID, 'searchFieldx')
book_info={'title': '食南之徒', 'author': '马伯庸', 'date': '2024-4-1', 'publisher': '湖南文艺出版社', 'url': 'https://book.douban.com/subject/36710597/'}
query_content = f'{book_info["title"]} {book_info["author"]}'
search_input.send_keys(query_content)
search_input.send_keys(Keys.RETURN)
browser.implicitly_wait(10)
h3_element = browser.find_element(By.XPATH, '//h3[@itemprop="name"]')
h3_child_a = h3_element.find_element(By.TAG_NAME, 'a')
book_detail_url= h3_child_a.get_attribute('href')
browser.get(book_detail_url)
browser.implicitly_wait(10)
download_button = browser.find_element(By.XPATH, '//a[@class="btn btn-primary addDownloadedBook"]')
download_link = download_button.get_attribute('href')
browser.get(download_link)
input()
browser.quit()