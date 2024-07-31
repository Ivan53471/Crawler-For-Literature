import re
from tqdm import tqdm
from get_keywords import get_keywords

# keywords是一个包含与化学相关的关键词的set
keywords = get_keywords()

# 逐行读取大文件
# 此处使用yield定义一个生成器函数
# 生成器函数可以暂停执行并返回一个值，然后在需要时继续执行
# 继续执行的判断逻辑包含在调用该函数的for循环中
def read_large_file(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

# 判断当前主题是否和化学相关
def is_chemistry_related(title):
    return any(keyword in title for keyword in keywords)

# 在已有词条中获取和化学相关的词条
def save_selected_text():
    with open('E:\wiki_cn_dataset\selected_wiki.txt', 'w', encoding='utf-8') as output_file:
        current_entry = []
        chemistry_related = False

        # 计数器初始化
        article_count = 0  
        # 初始化进度条
        progress_bar = tqdm(read_large_file('E:\wiki_cn_dataset\wiki.txt'), desc=u'已获取0篇文章')  
        # 使用 tqdm 包装 read_large_file 生成器，显示进度条
        for line in progress_bar:
            if re.match(r'【.+】', line):
                # 计数器加1
                article_count += 1
                # 如果当前词条非空，且与化学相关，则写入输出文件
                if chemistry_related and current_entry:
                    output_file.write('\n'.join(current_entry) + '\n\n\n')

                # 开始新的词条
                current_entry = [line]
                # 判断新的一级标题是否与化学相关
                chemistry_related = is_chemistry_related(line)
            else:
                # 添加到当前词条
                current_entry.append(line)
            
            # 更新进度条描述
            if article_count % 100 == 0:
                progress_bar.set_description(u'已获取%s篇文章' % article_count)  
        
        # 每次循环相当于处理前一次的词条，所以最后一个词条需要单独处理
        # 处理最后一个词条
        if chemistry_related and current_entry:
            output_file.write('\n'.join(current_entry) + '\n')