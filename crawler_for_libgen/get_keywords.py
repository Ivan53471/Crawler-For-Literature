# 从txt文件中读取关键词，并存储到一个set中
def get_keywords():
    with open('../keywords.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容
        content = file.read()
        # 用逗号分隔关键词，并去除空白字符
        keywords = {keyword.strip() for keyword in content.split(',')}
    return keywords