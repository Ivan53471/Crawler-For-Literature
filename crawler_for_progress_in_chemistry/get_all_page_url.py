from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_all_page_url(driver):

    # 使用XPATH定位到表格
    table_element = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[12]/div/div/section/div/div[4]/table'))
    )

    # 存储期刊每一期的链接
    literature_urls = []

    # 遍历表格的行（tr标签）
    rows = table_element.find_elements(By.TAG_NAME, 'tr')
    # 遍历表格的行（tr标签）
    for row in rows:
        # 遍历行的每个单元格（td标签）
        for cell in row.find_elements(By.TAG_NAME, 'td'):
            # 尝试获取单元格中a标签的href属性
            try:
                link = cell.find_element(By.TAG_NAME, 'a').get_attribute('href')
                # 如果链接存在，将其添加到行的数据列表中
                if link:
                    literature_urls.append(link)
            except:
                pass

    # print(literature_urls)
    return literature_urls
