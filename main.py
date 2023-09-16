from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option("detach", True)

service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.get("https://google.com")
browser.maximize_window()
search_bar = browser.find_element(By.NAME, "q")
search_bar.send_keys("flutter")
search_bar.send_keys(Keys.ENTER)

# search_results = browser.find_elements(By.CLASS_NAME, "yuRUbf")
# print(search_results)

try:
    # * 20s(페이지를 다 로딩할 때까지의 시간이 필요하다.) => 그래야 class_name을 찾는다. ✅
    search_results = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
    )
    print(f"총 결과값은 {len(search_results)}개 입니다.")
except Exception:
    print("불러오지 못했습니다.")

search_results.pop()

# * "MjjYud" class 내에서 <h3> 추출
for search_result in search_results:
    try:
        title = WebDriverWait(search_result, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h3"))
        )
        print(title.text)
    except Exception:
        print("불러오지 못했습니다.")

browser.quit()
