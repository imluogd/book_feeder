from utils import get_popular_book,get_new_books,search_zlib
from mail_utils import send_mail
'''
功能：
    1.爬取
        a.豆瓣新书速递（https://book.douban.com/latest?subcat=%E5%85%A8%E9%83%A8）
        b.一周热门图书榜
    2.搜索
        在zlibrary上搜索（能不能搜？）-需要代理
        '''
# for book in get_popular_book():
#     print(f'title:{book["title"]}, author:{book["author"]}')
#     search_zlib(book)
#     break
#test_info1={'title': '不理想的妻子', 'author': '王欣', 'date': '2024-4', 'publisher': '人民文学出版社', 'url': 'https://book.douban.com/subject/36866737/'}
#test_info2={'title': '食南之徒', 'author': '马伯庸', 'date': '2024-4-1', 'publisher': '湖南文艺出版社', 'url': 'https://book.douban.com/subject/36710597/'}
#search_zlib(test_info2)
