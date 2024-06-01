import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

session = requests.Session()
# 更新请求头信息以更接近浏览器的行为
_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

# 登录页面的 URL
login_url = 'https://zh.singlelogin.re'

# 获取登录页面，提取必要的隐藏字段（如果有）
login_page = session.get(login_url, headers=_headers)
soup = BeautifulSoup(login_page.text, 'html.parser')

# 如果登录表单中有隐藏字段，需要提取出来
hidden_fields = soup.find_all("input", type="hidden")
hidden_data = {field.get('name'): field.get('value') for field in hidden_fields}

# 登录表单数据
login_data = {
    'email': '1375472577@qq.com',  # 替换为您的邮箱
    'password': 'luoguangda1',        # 替换为您的密码
}
login_data.update(hidden_data)

# 将 cookie 字典转换为 CookieJar 对象
cookies_dict = {
    'remix_userid': '14398547',
    'remix_userkey': 'a5d4ec607a58fb7eed54fe10f723852d',
    'selectedSiteMode': 'books'
}
cookiejar = requests.utils.cookiejar_from_dict(cookies_dict)

# 将 CookieJar 对象设置为会话的 cookie
session.cookies = cookiejar

# 发送 POST 请求进行登录
response = session.post(login_url, data=login_data, headers=_headers)
response.raise_for_status()

if "Logout" in response.text:
    print("登录成功")
    test_info2 = test_info2={'title': '食南之徒', 'author': '马伯庸', 'date': '2024-4-1', 'publisher': '湖南文艺出版社', 'url': 'https://book.douban.com/subject/36710597/'}
    book_title = test_info2['title']
    book_author = test_info2['author']
    encoded_title = quote(book_title)
    encoded_author = quote(book_author)
    search_url = 'https://zh.singlelogin.re/s' + f'/?q={encoded_title}+{encoded_author}'
    #print(f"search_url：{search_url}")
    response = session.get(search_url, headers=_headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_href = soup.find('h3', itemprop="name").find('a')['href']
    full_link = 'https://zh.singlelogin.re' + link_href
    print(f"full_link：{full_link}")
    _new_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': 'remix_userkey=a5d4ec607a58fb7eed54fe10f723852d; remix_userid=14398547; selectedSiteMode=books; domainsNotWorking=zlibrary-asia.se',
    'Referer': search_url,
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}
    detail_page_response = session.get(full_link, headers=_new_headers)
    detail_page_response.raise_for_status()
    detail_soup = BeautifulSoup(detail_page_response.text, 'html.parser')
    #print(detail_page_response.text)
    download_link_tag = soup.find('a', class_='addDownloadedBook')
    download_href = download_link_tag['href']
    full_download_url = f'https://zh.singlelogin.re{download_href}'
    print("完整下载链接:", full_download_url)
else:
    print("登录zlibrary失败")
