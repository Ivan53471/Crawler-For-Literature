from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
from get_all_page_url import get_all_page_url
import time

def get_pdf_url_from_logs(logs):
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if 'Page.frameScheduledNavigation' in log['method']:
            url = log['params']['url']
            if 'pdf' in url.lower() and 'token' in url:
                return url
    return None

def get_download_urls(driver):
    download_urls = []
    try:
        literature_urls = get_all_page_url(driver=driver)
        # 遍历每一个链接
        count = 0
        for url in literature_urls:
            count += 1
            if count > 10:
                break
            # 访问该链接
            driver.get(url)
            time.sleep(3)
            # 找pdf下载按钮
            # 等待页面加载完成并找到指定的ul元素
            ul_element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.article-list'))
            )

            # 查找ul元素下的所有li标签
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

            # 清除以前的日志
            driver.get_log('performance')
            
            for li in li_elements:
                id = li.get_attribute('id')
                
                # 点击PDF下载按钮
                WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, f'//*[@id="{id}"]/div[2]/div[4]/span[2]/a'))
                ).click()
                
                time.sleep(1)

                 # 获取网络日志
                logs = driver.get_log('performance')

                # 从日志中提取PDF下载链接
                pdf_url = get_pdf_url_from_logs(logs)
                if pdf_url:
                    download_urls.append(pdf_url)

        return download_urls
    except Exception:
        return []
