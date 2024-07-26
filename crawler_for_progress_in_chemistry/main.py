from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from driver_init import driver_init
from get_download_urls import get_download_urls

def main():
    driver = driver_init(download_dir='D:/实习/苏州实验室/progress_in_chemistry')
    
    # 访问过刊浏览界面，该界面包含所有文章的链接
    driver.get("https://manu56.magtech.com.cn/progchem/CN/archive_by_years")
    time.sleep(3)
    download_urls = get_download_urls(driver=driver)
    if download_urls:
        print(download_urls)
    # 退出浏览器
    driver.quit()

if __name__ == "__main__":
    main()
