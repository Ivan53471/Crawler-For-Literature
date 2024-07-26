from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
from get_all_page_url import get_all_page_url
from WebDriverPool import *

# 从log中提取出pdf的下载url
def get_pdf_url_from_logs(logs):
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if 'Page.frameScheduledNavigation' in log['method']:
            url = log['params']['url']
            if 'pdf' in url.lower() and 'token' in url:
                return url
    return None

# 处理期刊单期的界面，需要完成：获取页面内容，点击下载按钮
def process_url(url, driver, pool):
    try:
        # 访问页面
        driver.get(url)
        time.sleep(3)
        print(f"Page loaded: {url}")

        # 等待页面加载完成并找到包含文章的ul元素
        ul_element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.article-list'))
        )

        # 查找ul元素下的所有li标签
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        # 清除以前的日志
        # driver.get_log('performance')  
        
        for li in li_elements:
            id = li.get_attribute('id')
            
            # 点击PDF下载按钮
            WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="{id}"]/div[2]/div[4]/span[2]/a'))
            ).click()
            
            time.sleep(1)
            # # 获取网络日志，并清除已有的网络日志
            # logs = driver.get_log('performance') 
            # # 从日志中提取PDF下载链接
            # pdf_url = get_pdf_url_from_logs(logs)  
            # if pdf_url:
            #     download_urls.append(pdf_url)
            #     # print(f"Found PDF URL: {pdf_url}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    
    finally:
        pool.return_driver(driver)
        print("end")

# 下载文件
def download():
    literature_urls = get_all_page_url()  # 获取所有页面URL
    print(len(literature_urls))
    # 使用WebDriverPool复用WebDriver实例
    max_workers = 3
    pool = WebDriverPool(max_workers, 'D:\实习\苏州实验室\progress_in_chemistry')
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 创建一个空字典来存储Future对象及其对应的WebDriver实例
        # futures = {}
        for url in literature_urls:
            # 后面的任务由于不能获得driver，会阻塞在这里
            driver = pool.get_driver()
            # 提交process_url任务给线程池
            # futures[executor.submit(process_url, url, driver, pool)] = driver
            executor.submit(process_url, url, driver, pool)
        
        # # 迭代处理每个已完成的Future对象
        # for future in as_completed(futures):
        #     # 获取与该Future对象对应的WebDriver实例
        #     driver = futures[future]
        #     try:
        #         # 获取每个future的结果
        #         # result = future.result() 
                
        #         # 将结果添加到下载链接列表中
        #         # download_urls.extend(result)
        #         # 等待任务完成
        #         future.result()
        #         print("finished")  
                
        #     except Exception as e:
        #         print(f"Error with future: {e}")
                

    pool.close_all()
