from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from login import login

def search(driver, theme):
    # 访问中国知网
    driver.get('https://www.cnki.net')
    
    # # 设置所需篇数
    # papers_need = 100
    # 等待页面加载完成，然后登录
    time.sleep(3)
    login(driver=driver)

    # 等待页面加载完成，并找到搜索框
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txt_SearchText'))
    ).send_keys(theme)

    # 点击搜索按钮
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/input[2]'))
    ).click()

    # 等待搜索结果加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'list-item'))
    )

    # 点击切换中文文献
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH ,'//*[@id="ModuleSearch"]/div[2]/div/div/div/div/a[1]'))
    ).click()
    time.sleep(1)

    # 获取总文献数和页数
    res_unm = WebDriverWait( driver, 100 ).until( 
        EC.presence_of_element_located((By.XPATH ,'//*[@id="countPageDiv"]/span[1]/em')) 
    ).text
    # 去除千分位里的逗号
    res_unm = int(res_unm.replace(",",''))
    page_unm = int(res_unm/20) + 1
    return page_unm