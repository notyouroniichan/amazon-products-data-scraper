import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import locale
from bs4 import BeautifulSoup

def convert_to_float(value):
    try:
        return float(locale.atof(value.replace(',', '')))
    except ValueError:
        return None

def read_short_names(file_path='Short_Names.txt'):
    try:
        with open(file_path, 'r') as file:
            data = file.read().strip()
            return [name.strip() for name in data[1:-1].replace("'", "").replace('"','').split(',')]
    except:
        return []

def setup_driver():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return uc.Chrome(options=options)
    except:
        return None

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return float(soup.find(class_="a-icon-alt").get_text()[:3]) if soup.find(class_="a-icon-alt") else 'No rating !',int(soup.find('u').get_text()[:3]) if soup.find('u') else 'No product option !'


def extract_product_data(product, page_num):
    try:
        company = product.find_element(By.XPATH, ".//span[@class='a-size-base-plus a-color-base']").text if product.find_elements(By.XPATH, ".//span[@class='a-size-base-plus a-color-base']") else ""
        sponsored = 'Yes' if product.find_elements(By.XPATH, ".//span[@class='a-color-secondary']") else 'No'
        rating,product_options = parse_html(product.find_element(By.XPATH, ".//span[@class='a-declarative']").get_attribute('outerHTML')) if product.find_elements(By.XPATH, ".//span[@class='a-declarative']") else 'No rating !'
        title = product.find_element(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']").text if product.find_elements(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']") else 'No product Name'
        price = convert_to_float(product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text) if product.find_elements(By.XPATH, ".//span[@class='a-price-whole']") else 'No price'
        no_of_ratings = convert_to_float(product.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text) if product.find_elements(By.XPATH, ".//span[@class='a-size-base s-underline-text']") else 'No rating provided !'
        delivery = product.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[5]/div/div/div/div/span/div/div/div[2]/div[5]/div/span').text if product.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[5]/div/div/div/div/span/div/div/div[2]/div[5]/div/span') else 'Free delivery not applicable !'
    except Exception as e:
        print(e)
    return {'Page': page_num, 'Company': company, 'Product Name': title, 'Price': price, 'Sponsored (Yes/No)': sponsored,'Rating out of 5': rating, 'Number of Global Ratings': no_of_ratings, 'Number of product options': product_options, 'Delivery Type': delivery}    

def scrape_page(driver, query, page_num):
    try:
        driver.get(f"https://www.amazon.in/s?k={query}&page={page_num}")
        time.sleep(2)
        products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
        return [extract_product_data(product, page_num) for product in products if product]
    except:
        return []

def scrape_product_info(driver, short_name):
    all_products = [scrape_page(driver, short_name, page_num) for page_num in range(1, 4)]
    all_product = [item for sublist in all_products for item in sublist]
    if all_product:
        pd.DataFrame(all_product).to_csv(f"output_files/{short_name}.csv", index=False)

def scrape_multiple_queries(short_names):
    driver = setup_driver()
    if driver:
        for short_name in short_names:
            scrape_product_info(driver, short_name)
        driver.quit()

if __name__ == "__main__":
    short_names = read_short_names('Short_Names.txt')
    if short_names:
        scrape_multiple_queries(short_names)
