from urllib.request import urlretrieve

def download():
    with open('literature_urls.txt', 'r', encoding='utf-8') as file:
            # 逐行读取文件内容
            lines = file.readlines()

    # 处理每个URL
    for line in lines:
        url = line.strip()
        # 下载文件
        urlretrieve(url)


# 后缀 .epub 出现了 99 次
# 后缀 .pdf 出现了 906 次
# 后缀 .mobi 出现了 69 次
# 后缀 .azw3 出现了 39 次
# 后缀 .zip 出现了 9 次
# 后缀 .chm 出现了 3 次
# 本代码并没有对除pdf外的其他后缀文件做转换处理