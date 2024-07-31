# 调用已有的libgen_scraper库，里面封装了对libgen库的搜索
import libgen_scraper as lg
from get_keywords import get_keywords

# 查询到所有链接后调用，将链接暂存在数组中
non_fiction_links = []
# article_links = []

def collect_non_fiction_download_links(non_fictions):
    for i in range(len(non_fictions)):
        links = non_fictions.download_links(i)
        non_fiction_links.extend(links)

# def collect_article_download_links(articles):
#     for i in range(len(articles)):
#         links = articles.download_links(i)
#         article_links.extend(links)

# 获取所有文件的下载链接
def get_download_links():

    for keyword in get_keywords():
        
        # 调用non_fiction查询接口
        non_fictions = lg.search_non_fiction(
            query=keyword,
            # search_in_fields=lg.NonFictionSearchField.TITLE,
            filter={
                lg.NonFictionColumns.LANGUAGE: r'Chinese',
            },
            limit=300,
        )

        collect_non_fiction_download_links(non_fictions)

        # 论文无法筛选论文，先不考虑
        # # 调用论文查询接口
        # articles = lg.search_articles(
        #     query=keyword,
        #     filter={
        #         lg.ArticlesColumns.LANGUAGE: r'Chinese',
        #     },
        #     limit=200,
        # )

        # collect_article_download_links(articles)

    # return non_fiction_links + article_links
    return non_fiction_links


def save_all_download_links():
    literature_urls = get_download_links()
    with open('literature_urls.txt', 'w', encoding='utf-8') as file:
            for url in literature_urls:
                file.write(url + '\n')