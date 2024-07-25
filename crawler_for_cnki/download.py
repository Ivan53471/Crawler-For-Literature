from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download(driver, link):
    try:
        # 访问文献页面
        driver.get(link)

        time.sleep(3)
        # 点击PDF下载按钮
        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pdfDown"]'))
        ).click()

        # 等待下载完成
        time.sleep(3)
        return True
    except Exception:
        return False
