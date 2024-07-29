import queue
from tools.driver_init import driver_init

# WebDriver实例池，实现复用实例，减少重复创建与销毁的开销
# pool中存放着没有被使用的driver
class WebDriverPool:
    def __init__(self, max_size, download_dir):
        self.pool = queue.Queue(maxsize=max_size)
        for _ in range(max_size):
            self.pool.put(driver_init(download_dir))

    def get_driver(self):
        return self.pool.get()

    def return_driver(self, driver):
        self.pool.put(driver)

    def close_all(self):
        while not self.pool.empty():
            driver = self.pool.get()
            driver.quit()