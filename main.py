from package.helpers import browser_settings
from selenium.webdriver.common.by import By
from time import sleep
from os import mkdir
from os.path import join, exists
import pandas as pd

# CREATE FOLDER
initial_route = "."
folder_path = join(initial_route, "data")
if not exists(folder_path):
    mkdir(folder_path)

# BROWSER SETTINGS
driver = browser_settings(download=True, headless=False)

# THE WBPAGE URL
url = "https://comprar.pediasure.abbott/pe/"
driver.get(url)
sleep(2)

# SCRAPING

# -- close popup modal
xpath_popup = '//div[contains(@class, "first-purchase-popup")]/button[@class="closebtn"]'
popup = driver.find_element(By.XPATH, xpath_popup)

if popup:
    popup.click()

# -- select category "polvo"
category_name = 'Polvo'
xpath_category = f'//div/nav[contains(@class, "sw-megamenu")]/ul//li//a[@title="Polvo"]'
category = driver.find_element(By.XPATH, xpath_category)

if category:
    category.click()

data = []

# -- get products
xpath_li = '//div[@id="layer-product-list"]/div[contains(@class, "products")]/ol//li'
elements_li = driver.find_elements(By.XPATH, xpath_li)

if len(elements_li) > 0 :
    for e_product in elements_li :
        dict_data = {}

        # GET DIV
        xpath_product_info = './div[contains(@class, "product-item-info")]'
        element_info = e_product.find_element(By.XPATH, xpath_product_info)

        # GET PRODUCT DETAILS
        # -- idproduct
        id_product = element_info.get_attribute("data-productid")
        dict_data['id_product'] = id_product

        # -- name
        xpath_name = './div[contains(@class, "product-item-details")]/strong/a'
        product_name = element_info.find_element(By.XPATH, xpath_name).text
        dict_data['product_name'] = product_name

        # -- old price
        xpath_price_old = './div[contains(@class, "product-item-details")]/div[contains(@class, "price-box")]/span[@class="old-price"]'
        product_old_price = element_info.find_element(By.XPATH, xpath_price_old).text
        dict_data['product_old_price'] = product_old_price if product_old_price else ''

        # -- current price
        value_id_attribute = f"product-price-{id_product}"

        xpath_elment_price = f'//*[@id="{value_id_attribute}"]'
        product_price = element_info.find_element(By.XPATH, xpath_elment_price).text
        dict_data['product_price'] = product_price if product_price else ''

        # -- link product
        xpath_link_product = './div[contains(@class, "product-item-photo")]/a'
        element_link_product = element_info.find_element(By.XPATH, xpath_link_product)
        link_product =  element_link_product.get_attribute('href')
        dict_data['link_product'] = link_product

        # -- image product
        xpath_image_product = './div[contains(@class, "product-item-photo")]/a//img'
        element_image_product = element_info.find_elements(By.XPATH, xpath_image_product)
        link_image = element_image_product[0].get_attribute('src')
        dict_data['link_image'] = link_image

        data.append(dict_data)

# FORMAT CSV
path = join(folder_path, "products_data.csv")
df_products = pd.DataFrame.from_dict(data)
products_csv = df_products.to_csv(path, header=True, index=False)

print("data saved in: ", path)

sleep(3)
driver.close()
driver.quit()