from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import json
import queue
import time
from get_all_page_url import get_all_page_url
from WebDriverPool import *

# 从log中提取出pdf的下载url
def get_pdf_url_from_logs(logs):
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if 'Page.frameScheduledNavigation' in log['method']:
            url = log['params']['url']
            if 'pdf' in url.lower() and 'id' in url.lower():
                return url
    return None

# 处理期刊单期的界面，需要完成：获取页面内容，点击下载按钮
def process_url(url, driver, pool, all_download_urls):
    try:
        # 访问页面
        driver.get(url)
        time.sleep(3)
        print(f"Page loaded: {url}")

        # 等待页面加载完成并找到包含文章的ul元素
        ul_element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[2]/ul'))
        )
        
        # 找到ul元素下所有id以"art"开头的div元素
        div_elements = ul_element.find_elements(By.XPATH, ".//div[starts-with(@id, 'art')]")

        download_urls = []
        for div in div_elements[1:]:
            id = div.get_attribute('id')
            # 查找li元素下的PDF按钮
            WebDriverWait(div, 100).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="{id}"]/div/dl/div[2]/dd[4]/a[3]'))
            ).click()
            time.sleep(1)

            # 获取网络日志，并清除已有的网络日志
            logs = driver.get_log('performance') 
            # print(logs)
            # 从日志中提取PDF下载链接
            pdf_url = get_pdf_url_from_logs(logs)  
            if pdf_url:
                download_urls.append(pdf_url)
                # print(f"Found PDF URL: {pdf_url}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    
    finally:
        pool.return_driver(driver)
        # 处理完成后，将找到的PDF URLs批量放入队列
        for url in download_urls:
            all_download_urls.put(url)
        # print("end")

def write_to_file(all_download_urls):
    # 打开一个文件以写入
    with open('download_urls.txt', 'w') as file:
        while not all_download_urls.empty():
            url = all_download_urls.get()
            # 写入每个PDF URL，并加上换行符
            file.write(url + '\n')  

# 下载文件
def save_download_urls():
    literature_urls = get_all_page_url()  # 获取所有页面URL
    print(len(literature_urls))
    all_download_urls = queue.Queue()
    # 使用WebDriverPool复用WebDriver实例
    max_workers = 10
    pool = WebDriverPool(max_workers, 'E:/crawler_download/applied_chemistry')
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 创建一个空字典来存储Future对象及其对应的WebDriver实例
        # futures = {}
        for url in literature_urls:
            # 后面的任务由于不能获得driver，会阻塞在这里
            driver = pool.get_driver()
            # 清除无关log
            driver.get_log('performance') 
            # 提交process_url任务给线程池
            executor.submit(process_url, url, driver, pool, all_download_urls)

    pool.close_all()

    write_to_file(all_download_urls=all_download_urls)

save_download_urls()
