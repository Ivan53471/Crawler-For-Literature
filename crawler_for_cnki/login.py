from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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