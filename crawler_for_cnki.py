from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from driver_init import driver_init

def login(driver):

    # 账号密码
    username = "xxx"
    password = "xxx"

    # 点击个人登录按钮
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="headerBox"]/div/div[1]/div/div[1]/div[2]'))
    ).click()

    # 将账号密码填入弹出的登录界面
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="headerBox"]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/input'))
    ).send_keys(username)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="headerBox"]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/input'))
    ).send_keys(password)

    # 勾选同意协议按钮
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH ,'//*[@id="agreement"]'))
    ).click()
    
    # 点击登录按钮
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH ,'//*[@id="headerBox"]/div/div[1]/div/div[2]/div[2]/div[2]/button'))
    ).click()

    time.sleep(1)
    
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

def get_one_page_article_links(source_html):
    soup = BeautifulSoup(source_html, 'html.parser')

    # 提取文献链接
    articles = soup.find_all('a', class_='fz14', target='_blank')

    return articles

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


def get_abstract(driver, link):
    # 访问文献页面
    driver.get(link)

    time.sleep(3)

    # 获取abstract
    abstract = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ChDivSummary"]'))
    ).text
    return abstract
def main():
    driver = driver_init(download_dir='D:/实习/苏州实验室/cnki')
    theme = '化学'
    total_pages = search(driver=driver, theme=theme)
    
    # 指定要下载的页数
    specified_pages = 2

    for page in range(1, specified_pages + 1):
        articles = get_one_page_article_links(source_html=driver.page_source)
        
        for article in articles:
            link = article['href']
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


