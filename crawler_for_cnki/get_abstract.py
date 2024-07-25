from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_abstract(driver, link):
    # 访问文献页面
    driver.get(link)

    time.sleep(3)

    # 获取abstract
    abstract = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ChDivSummary"]'))
    ).text
    return abstract