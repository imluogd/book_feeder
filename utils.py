import requests
from bs4 import BeautifulSoup
import re
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
    

#api
