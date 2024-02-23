from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Browser settings
def browser_settings(download=True, headless=True):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument('--headless')

    options.add_argument('--no-sandbox') # not a test environment
    options.add_argument('--disable-dev-shm-usage') # docker instance
    options.add_argument('--disable-gpu') # not run script without opening the browser
    options.add_argument('--disable-notificacations')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')

    options.add_experimental_option('excludeSwitches', ['enable-logging']) # login mesages

    # OPTIONS TO ASSEMBLE THE DRIVER
    if download:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else :
        browser = webdriver.Chrome('chromedriver', options=options)

    return browser