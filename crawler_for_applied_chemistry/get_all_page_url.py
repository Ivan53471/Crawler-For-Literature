# 从已有的文件中读取literature_urls
def get_all_page_url():

    literature_urls = []
    with open('literature_urls.txt', 'r', encoding='utf-8') as file:
        for line in file:
            literature_urls.append(line.strip())  # 去除每行末尾的换行符并添加到列表中

    return literature_urls
