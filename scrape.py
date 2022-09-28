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
TINT_COLOR = (0, 0, 0)  # Black
TRANSPARENCY = .25  # Degree of transparency, 0-100%
OPACITY = int(255 * TRANSPARENCY)


class Scrape(object):

    def __init__(self):
        self.mobile_ss_name = f'{os.path.join("images", datetime.now().strftime("%Y%m%d-%H%M"))}_mobile.png'
        self.desktop_ss_name = f'{os.path.join("images", datetime.now().strftime("%Y%m%d-%H%M"))}_desktop.png'
        self.modified_date = None

    def get_desktop(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1080, 1920")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)

        self.modified_date = driver.find_element(By.XPATH, '//*[@id="modifiedDate"]').text.strip()
        driver.save_screenshot(f'{self.desktop_ss_name}')
        self.watermark(f'{self.desktop_ss_name}', "DESKTOP")
        driver.quit()

    def get_mobile(self):
        options = Options()
        options.headless = True

        mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "
                                         "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 "
                                         "Mobile Safari/535.19"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)
        driver.save_screenshot(f'{self.mobile_ss_name}')
        self.watermark(f'{self.mobile_ss_name}', "MOBILE")
        driver.quit()

    @staticmethod
    def watermark(img_file_name, test_mode):
        img = Image.open(img_file_name)
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("./fonts/roboto-mono-v22-latin-regular.ttf", 32)
        text = f'GOC.STORE {test_mode} TEST {datetime.now().strftime("%Y%m%d-%H%M")}'
        x, y = 350, 900
        w, h = font.getsize(text)

        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
        draw.rectangle((x, y, x + w, y + h), fill=TINT_COLOR + (OPACITY,))
        draw.text((x, y), text, (255, 0, 255), font=font)
        overlay = overlay.rotate(45)
        img = Image.alpha_composite(img, overlay)
        img = img.convert("RGB")  # Remove alpha for saving in jpg format.
        # draw.text((x, y),"Sample Text",(r,g,b))
        img.save(os.path.join(img_file_name))


if __name__ == '__main__':
    scraper = Scrape()
    scraper.get_desktop()
    scraper.get_mobile()
    modified_date = scraper.modified_date
    print(modified_date)
    print(scraper.desktop_ss_name)
    print(scraper.mobile_ss_name)
