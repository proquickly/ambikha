from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

# Initialize the WebDriver (assuming you have ChromeDriver installed and in your PATH)
driver = webdriver.Chrome()

# Open the HTML file
driver.get("file:///Users/andy/ws/lessons/ambikha/purchase_product.html")

# Test: Select purchase option
select = Select(driver.find_element(By.ID, "purchase_option"))
select.select_by_value("purchase")

# Test: Enter product to search
search_product = driver.find_element(By.ID, "search_product")
search_product.send_keys("Example Product")

# Test: Add product to cart
add_to_cart = driver.find_element(By.ID, "add_to_cart")
add_to_cart.send_keys("2")

# Test: Order product
order_product = driver.find_element(By.ID, "order_product")
order_product.send_keys("Order Example Product")

# Submit the form
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
submit_button.click()

# Wait for a few seconds to observe the result
time.sleep(5)

# Close the browser
driver.quit()