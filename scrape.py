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
TRANSPARENCY = .35  # Degree of transparency, 0-100%
OPACITY = int(255 * TRANSPARENCY)
XPATH = '//*[@id="modifiedDate"]'
FONT = "./fonts/roboto-mono-v22-latin-regular.ttf"
FORMAT = "%Y%m%d-%H%M"
SS_PATH = "./images"


class Scrape(object):

    def __init__(self):
        self.process_date = datetime.now().strftime(FORMAT)
        self.ss_prefix = os.path.join(SS_PATH, self.process_date)
        # Mobile Screen Shot Path
        self.m_ss_path = f"{self.ss_prefix}_mobile.png"
        # Desktop Screen Shot Path
        self.dd_ss_path = f"{self.ss_prefix}_desktop.png"
        self.modified_date = None

    def get_desktop(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1080, 1920")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)

        self.modified_date = driver.find_element(By.XPATH, XPATH).text.strip()
        driver.save_screenshot(f'{self.dd_ss_path}')
        self.watermark(f'{self.dd_ss_path}', "DESKTOP")
        driver.quit()

    def get_mobile(self):
        options = Options()
        options.headless = True

        mobile_emulation = {"deviceMetrics": {"width": 360,
                                              "height": 640,
                                              "pixelRatio": 3.0},
                            "userAgent": "Mozilla/5.0 "
                                         "(Linux; Android 4.2.1; en-us; "
                                         "Nexus 5 Build/JOP40D) "
                                         "AppleWebKit/535.19 "
                                         "(KHTML, like Gecko) "
                                         "Chrome/18.0.1025.166 "
                                         "Mobile Safari/535.19"}

        options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(URL)
        driver.save_screenshot(f'{self.m_ss_path}')
        self.watermark(f'{self.m_ss_path}', "MOBILE")
        driver.quit()

    def watermark(self, img_file_name, test_mode):
        """Watermark the screenshots for the visual comparison purposes"""
        img = Image.open(img_file_name)

        font = ImageFont.truetype(FONT, 50)

        text = f'GOC.STORE {test_mode} ' \
               f'TEST {self.process_date}'

        x, y = 5, 900
        w, h = font.getsize(text)

        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        # Create a context for drawing things on it
        draw = ImageDraw.Draw(overlay)
        draw.rectangle((x, y, x + w, y + h), fill=TINT_COLOR + (OPACITY,))
        draw.text((x, y), text, (255, 255, 0), font=font)

        overlay = overlay.rotate(45)
        img = Image.alpha_composite(img, overlay)
        # Remove alpha for saving in jpg format.
        img = img.convert("RGB")  # Remove alpha for saving in jpg format.
        img.save(os.path.join(img_file_name))


if __name__ == '__main__':
    scraper = Scrape()
    scraper.get_desktop()
    scraper.get_mobile()
    modified_date = scraper.modified_date
    print(modified_date)
    print(scraper.dd_ss_path)
    print(scraper.m_ss_path)
