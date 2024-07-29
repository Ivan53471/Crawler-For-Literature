from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tools.driver_init import driver_init
from search import search
from get_one_page_article_links import get_one_page_article_links
from download import download

def main():
    driver = driver_init(download_dir='D:/实习/苏州实验室/cnki')
    theme = '化学'
    total_pages = search(driver=driver, theme=theme)
    
    # 指定要下载的页数
    specified_pages = 2

    for page in range(1, specified_pages + 1):
        articles = get_one_page_article_links(source_html=driver.page_source)
        
        for article in articles:
            # 文献访问链接
            link = article['href']
            # 判断是否下载成功
            if not download(driver=driver, link=link):
                print(f"Failed to download: {link}")

        if page < specified_pages:
            # 点击下一页按钮
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="PageNext"]'))
            ).click()
            time.sleep(3)  # 等待页面加载

    # 关闭浏览器
    driver.quit()

if __name__ == "__main__":
    main()


