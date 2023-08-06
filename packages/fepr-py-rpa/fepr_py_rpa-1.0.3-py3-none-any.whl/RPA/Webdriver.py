from selenium import webdriver
import chromedriver_binary
from logging import getLogger

logger = getLogger(__name__)


def browser(save_dir: str, headless = False):
    # ダウンロード先指定
    prefs = {"download.default_directory": save_dir}

    # 各種オプション追加
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--lang=ja-JP')
    
    if headless == True:
        chrome_options.add_argument('--headless')

    return webdriver.Chrome(chrome_options=chrome_options)
