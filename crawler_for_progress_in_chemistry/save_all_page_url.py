from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver_init import driver_init
import time

def save_all_page_url():

    driver = driver_init(download_dir='D:/实习/苏州实验室/progress_in_chemistry')
    
    # 访问过刊浏览界面，该界面包含所有文章的链接
    driver.get("https://manu56.magtech.com.cn/progchem/CN/archive_by_years")

    time.sleep(3)

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
    
    # 退出浏览器
    driver.quit()

    # 将URL保存到txt文件中
    with open('literature_urls.txt', 'w', encoding='utf-8') as file:
        for url in literature_urls:
            file.write(url + '\n')

save_all_page_url()
