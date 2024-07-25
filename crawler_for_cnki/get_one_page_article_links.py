from bs4 import BeautifulSoup

# 获取一整页文献的访问链接
def get_one_page_article_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')

    # 提取文献链接
    articles = soup.find_all('a', class_='fz14', target='_blank')

    return articles