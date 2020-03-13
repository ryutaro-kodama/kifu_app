from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_binary

class OperateSelenium():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def viewPage(self, url):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def setCookies(self, cookies):
        for cookie in cookies:
            self.driver.execute_script(f'document.cookie = "{cookie}";')

    # target_idが表示するまでtime秒待機
    def wait(self, target_id, time):
        try:
            WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.ID, target_id)))
        except TimeoutException as e:
            print(e)
            print("予定していたIDが表示されませんでした")
            self.close()
            self.quit()

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()