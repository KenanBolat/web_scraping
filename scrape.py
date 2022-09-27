from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import os


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


URL = 'https://store.goc.gov.tr'
DRIVER_PATH = './chromedriver'


class Scrape(object):

    def __init__(self):
        self.mobile_ss_name = f'{os.path.join("images", datetime.now().strftime("%Y%m%d-%H%M"))}_mobile.png'
        self.desktop_ss_name = f'{os.path.join("images", datetime.now().strftime("%Y%m%d-%H%M"))}_desktop.png'
        self.modified_date = None

    def get_desktop(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1280, 1024")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)

        self.modified_date = driver.find_element(By.XPATH, '//*[@id="modifiedDate"]').text.strip()
        driver.save_screenshot(f'{self.desktop_ss_name}')



        img = Image.open(f'{self.desktop_ss_name}')
        rgb_im = img.convert('RGB')
        rgb_im.save(f'{self.desktop_ss_name}')
        img = Image.open(f'{self.desktop_ss_name}')
        draw = ImageDraw.Draw(img)


        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("./fonts/roboto-mono-v22-latin-regular.ttf", 45)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((50, 100), f'GOC.STORE DESKTOP TEST {datetime.now().strftime("%Y%m%d-%H%M")}', (255, 0, 255), font=font)
        img.save(os.path.join(f'{self.desktop_ss_name}'))


        driver.quit()

    def get_mobile(self):
        options = Options()
        options.headless = True
        mobile_emulation = {"deviceName": "Nexus 5"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)
        driver.save_screenshot(f'{self.mobile_ss_name}')

        img = Image.open(f'{self.mobile_ss_name}')
        rgb_im = img.convert('RGB')
        rgb_im.save(f'{self.mobile_ss_name}')
        img = Image.open(f'{self.mobile_ss_name}')
        draw = ImageDraw.Draw(img)


        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("./fonts/roboto-mono-v22-latin-regular.ttf", 45)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((50, 100), f'GOC.STORE MOBILE TEST {datetime.now().strftime("%Y%m%d-%H%M")}', (255, 0, 255), font=font)
        img.save(os.path.join(f'{self.mobile_ss_name}'))
        driver.quit()


if __name__ == '__main__':
    scraper = Scrape()
    scraper.get_desktop()
    scraper.get_mobile()
    modified_date = scraper.modified_date
    print(modified_date)
    print(scraper.desktop_ss_name)
    print(scraper.mobile_ss_name)


