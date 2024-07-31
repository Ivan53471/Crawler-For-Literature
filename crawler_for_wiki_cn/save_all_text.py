from gensim.corpora.wikicorpus import extract_pages,filter_wiki
import bz2
import re
from opencc import OpenCC 
from tqdm import tqdm
import codecs

# 提取维基百科文章
wiki_pages  = extract_pages(bz2.open('E:\wiki_cn_dataset\zhwiki-20240320-pages-articles-multistream.xml.bz2'))

# 初始化翻译器
openCC = OpenCC('t2s') 

def wiki_replace(page):
    # 获取文章内容
    content = page[1]  

    # 去除特定格式的内容
    content = re.sub(':*{\|[\s\S]*?\|}', '', content)
    content = re.sub('<gallery>[\s\S]*?</gallery>', '', content)
    content = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', content)
    # 过滤维基标记
    content = filter_wiki(content)  
    # 去除无用符号
    content = re.sub('\* *\n|\'{2,}', '', content)  
     # 合并多余的空行
    content = re.sub('\n+', '\n', content) 
    # 去除特定格式的换行
    content = re.sub('\n[:;]|\n +', '\n', content)  
    # 在标题前添加空行
    content = re.sub('\n==', '\n\n==', content)  
    # 在文章标题前后添加特殊符号
    content = u'【' + page[0] + u'】\n' + content  
    # 转换为简体中文并去除首尾空白
    return openCC.convert(content).strip()  

# 获取中文维基百科的所有文章，经过整理后，保存在wiki.txt文件中
def save_all_text():
    # 计数器初始化
    article_count = 0  
    # 打开输出文件
    output_file = codecs.open('E:\crawler_download\wiki_cn_dataset\wiki.txt', 'w', encoding='utf-8')  
    # 初始化进度条
    progress_bar = tqdm(wiki_pages, desc=u'已获取0篇文章')  

    # 遍历维基百科文章
    for page in progress_bar:
        # 过滤特定前缀的文章和空内容
        if not re.findall('^[a-zA-Z]+:', page[0]) and page[0] and not re.findall(u'^#', page[1]):
            # 处理文章内容
            cleaned_text = wiki_replace(page)  
            # 将处理后的内容写入文件
            output_file.write(cleaned_text + '\n\n\n')  
            # 计数器加1
            article_count += 1  
            # 更新进度条描述
            if article_count % 100 == 0:
                progress_bar.set_description(u'已获取%s篇文章' % article_count)  

    output_file.close()


# 原代码来源于以下文章，笔者只是对代码作一定整理，使得代码更易读懂
# @online{kexuefm-4176,
#         title={获取并处理中文维基百科语料},
#         author={苏剑林},
#         year={2017},
#         month={Jan},
#         url={\url{https://spaces.ac.cn/archives/4176}},
# }