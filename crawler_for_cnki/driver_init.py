from selenium import webdriver

def driver_init(download_dir):

    # 配置Chrome选项
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')  # 无头模式，不打开浏览器界面
    options.add_argument('--disable-gpu')
    # 设置chrome不加载图片，提高速度
    options.add_argument('blink-settings=imagesEnabled=false')

    prefs = {
        "download.default_directory": download_dir,  # 设置文件下载的默认目录为download_dir
        "download.prompt_for_download": False,       # 设置不弹出下载文件时的提示，自动下载文件
        "download.directory_upgrade": True,          # 如果下载目录不存在，自动创建
        "plugins.always_open_pdf_externally": True,  # 直接下载PDF文件，而不是在浏览器中打开
        "excludeSwitches": ["enable-automation"]     # 以开发者模式运行
    }
    options.add_experimental_option("prefs", prefs)

    # 创建浏览器驱动
    driver = webdriver.Chrome(options=options)

    return driver