from math import ceil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

BROWSER_HEIGHT = 857

chrome_options = Options()
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get("https://nomadcoders.co")
browser.maximize_window()

sizes = [480, 960, 1366, 1920]
print(browser.get_window_size())
for size in sizes:
    browser.set_window_size(size, BROWSER_HEIGHT)
    browser.execute_script("window.scrollTo(0,0)")
    # * js에서 python 으로 정보를 가져올 수 있다. return 을 넣어줘서
    time.sleep(5)
    scroll_size = browser.execute_script("return document.body.scrollHeight")
    total_sections = ceil(scroll_size / BROWSER_HEIGHT)
    for section in range(total_sections + 1):
        browser.execute_script(f"window.scrollTo(0, {(section) * BROWSER_HEIGHT})")
        browser.save_screenshot(f"screenshots/{size}x{section}.png")
        time.sleep(2)
