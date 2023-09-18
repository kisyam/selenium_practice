from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# * Chrome Sets
chrome_options = Options()
service = Service(executable_path=ChromeDriverManager().install())
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option("detach", True)


class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir, class_name, scroll_down_count):
        self.keyword = keyword
        self.class_name = class_name
        self.screenshots_dir = screenshots_dir
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        self.scroll_down_count = scroll_down_count

    def start(self):
        self.browser.get("https://google.com")
        # self.browser.maximize_window()

        # * search_bar 찾기
        search_bar = self.browser.find_element(By.NAME, "q")  # google search input name
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

    def take_screenshot(self):
        # * 다음 페이지 버튼이 사라지고 무한 스크롤 로딩 형식을 바뀌어서 JS로 스코를다운 명령을 보내주기로 했다.
        for i in range(self.scroll_down_count):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

        # * shitty_element 없을 경우가 있어서 예외처리를 해줘야 함.
        try:
            shitty_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cUnQKe"))
            )
            print(shitty_element)
            self.browser.execute_script(
                """
                const shitty = arguments[0];
                shitty.parentElement.removeChild(shitty);
            """,
                shitty_element,
            )
        except Exception:
            pass

        # * 20s(페이지를 다 로딩할 때까지의 시간이 필요하다.) => 그래야 class_name을 찾는다. ✅
        search_results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, self.class_name))
        )
        print(f"총 결과값은 {len(search_results)}개 입니다.")

        # * enumerate func : index 값도 가져와준다.
        for index, search_result in enumerate(search_results):
            search_result.screenshot(
                f"{self.screenshots_dir}/{self.keyword}x{index}.png"
            )
            print(f"{self.keyword}{index} download complete!")
            # title = WebDriverWait(search_result, 20).until(
            #     EC.presence_of_element_located((By.TAG_NAME, "h3"))
            # )
            # print(title.text)

    def finish(self):
        self.browser.quit()

        # search_results = browser.find_elements(By.CLASS_NAME, "yuRUbf")
        # print(search_results)


flutter_search = GoogleKeywordScreenshooter("flutter", "screenshots", "asEBEc", 3)
flutter_search.start()
flutter_search.take_screenshot()
flutter_search.finish()
