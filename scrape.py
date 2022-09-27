from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

URL = 'https://store.goc.gov.tr'
DRIVER_PATH = '/home/knn/PycharmProjects/check_file_modified_date/chromedriver'


class Scrape(object):

    def __init__(self):
        self.mobile_ss_name = f'{datetime.now().strftime("%Y%m%d-%H%M")}_mobile.png'
        self.desktop_ss_name = f'{datetime.now().strftime("%Y%m%d-%H%M")}_desktop.png'
        self.modified_date = None

    def get_desktop(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1280, 1024")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)

        self.modified_date = driver.find_element(By.XPATH, '//*[@id="modifiedDate"]').text.strip()
        driver.save_screenshot(f'{self.desktop_ss_name}')
        driver.quit()

    def get_mobile(self):
        options = Options()
        options.headless = True
        mobile_emulation = {"deviceName": "Nexus 5"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)
        driver.save_screenshot(f'{self.mobile_ss_name}')
        driver.quit()


if __name__ == '__main__':
    scraper = Scrape()
    scraper.get_desktop()
    scraper.get_mobile()
    modified_date = scraper.modified_date

