import re
from tqdm import tqdm
import threading
from queue import Queue
from get_keywords import get_keywords

# keywords是一个包含与化学相关的关键词的set
keywords = get_keywords()

# 逐行读取大文件
# 读取大文件并将数据块放入队列中
def read_large_file(file_path, queue):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            current_entry = []
            # cnt = 0
            for line in file:
                line = line.strip()
                if re.match(r'【.+】', line):
                    if current_entry:
                        queue.put(current_entry)
                        # cnt += 1
                        # if cnt % 100 == 0:
                        #     print(cnt)
                    current_entry = [line]
                else:
                    current_entry.append(line)
            # 处理最后一篇文章
            if current_entry:
                # 放入最后一篇文章
                queue.put(current_entry)
                # 放入结束信号，告知处理线程        
                queue.put(None)  
    except Exception as e:
        print(f"Error reading file: {e}")

# 处理队列中的数据块，检查是否与化学相关，并更新进度条
def process_entries(queue, progress):
    while True:
        entry = queue.get()
        # 接收到结束信号
        if entry is None: 
            # 确保所有线程都收到结束信号
            queue.put(None)  
            break
        
        try:
            full_text = '\n'.join(entry)
            # 判断规则：所有关键词在词条全文中出现的次数总和大于80次
            count = sum(full_text.count(keyword) for keyword in keywords)
            if count > 80:
                save_entry(entry)
            # 确保进度条更新是线程安全的    
            with progress.get_lock():  
                progress.update(1)
        except Exception as e:
            print(f"Error processing entry: {e}")

# 处理题目中出现的不允许的字符
def clean_filename(filename):
    # 使用正则表达式替换Windows和Unix系统中不允许的文件名字符
    return re.sub(r'[\<\>\:\"\/\\\|\?\*\0]', '_', filename)

# 将符合条件的条目保存到文件
def save_entry(entry):
    try:
        title = entry[0].strip('【】')
        # 清理文件名中的非法字符
        cleaned_title = clean_filename(title)
        path = f'E:\\crawler_download\\wiki_cn_selected_dataset\\{cleaned_title}.txt'
        with open(path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(entry))
    except Exception as e:
        print(f"Error saving files: {e}")

# 在已有词条中获取和化学相关的词条
def save_selected_text():
    # 初始化一个线程安全的队列
    queue = Queue()  
    file_path = 'E:\\crawler_download\\wiki_cn_dataset\\wiki.txt'
    
    # 创建进度条
    progress = tqdm(desc="处理词条进度", unit="条")

    # 启动一个线程用于读取文件
    reader_thread = threading.Thread(target=read_large_file, args=(file_path, queue))
    reader_thread.start()
    
    # 启动多个工作线程进行数据处理
    num_workers = 30
    workers = []
    for _ in range(num_workers):
        worker = threading.Thread(target=process_entries, args=(queue, progress))
        worker.start()
        workers.append(worker)

    # 等待所有处理线程结束  
    reader_thread.join()  
    for worker in workers:
        worker.join()
    
    progress.close()  # 关闭进度条

save_selected_text()
