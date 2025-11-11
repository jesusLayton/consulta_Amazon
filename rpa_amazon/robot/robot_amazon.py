from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

class AmazonRobot:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
        self.products_data = pd.read_excel('robot/productos.xlsx')

    def search_product(self, product_name):
        self.driver.get('https://www.amazon.com')
        search_box = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for results to load

    def extract_product_info(self):
        products = self.driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')
        product_info = []

        for product in products:
            title = product.find_element(By.CSS_SELECTOR, 'h2 .a-link-normal').text
            try:
                price = product.find_element(By.CSS_SELECTOR, '.a-price .a-offscreen').text
            except:
                price = 'N/A'
            product_info.append({'title': title, 'price': price})

        return product_info

    def save_to_excel(self, data):
        df = pd.DataFrame(data)
        df.to_excel('robot/extracted_products.xlsx', index=False)

    def run(self):
        for index, row in self.products_data.iterrows():
            self.search_product(row['Product Name'])
            product_info = self.extract_product_info()
            self.save_to_excel(product_info)
            time.sleep(2)  # Wait before the next search

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    robot = AmazonRobot()
    try:
        robot.run()
    finally:
        robot.close()