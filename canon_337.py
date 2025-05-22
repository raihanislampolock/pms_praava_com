import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import traceback

from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True  # Optional: run in headless mode (no UI needed in Docker)

driver = webdriver.Firefox(options=options)

def get_cartridge_info():
    # Define the floor details as a dictionary with keys as floor names and values as dictionaries with floor info
    floor_details = {
        "Floor_1_Pharmacy_Black": {
            "url": "http://10.1.0.249/login.html",
            "ip": "10.1.0.249",
            "cartridge_xpath": "//div[@class='table_row']//td[2]//span[2]"
        },
    }

    floor_cartridge_details = dict()

    # Loop through each floor and get cartridge info
    for key, val in floor_details.items():
        try:
            # Open the webpage and wait for the element to be clickable before clicking it
            driver.get(val["url"])
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitButton"]')))
            element.click()

            # Get the HTML of the page and use BeautifulSoup to extract the cartridge info
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cartridge_level = soup.find('div', {'id': 'tonerInfomationModule'}).findChildren("td")[0].text
            number = re.findall(r'\d+', cartridge_level)[0]  # Use raw string for regex
            message_div = soup.find("span", {"class": "StatusMessage"})
            for span in message_div:
                span_text = span.text

            # Add the cartridge info to the dictionary
            percent = {"black": number}
            floor_cartridge_details[key] = {
                "ip": val["ip"],
                "percentage": percent,
                "status": "online",
                "device_status": span_text
            }

        except Exception as e:
            # Print an error message if there was an issue getting the cartridge info
            print(f"Error retrieving cartridge info for {key}: {str(e)}")
            # Uncomment the following line to print the full traceback
            # print(traceback.format_exc())

    # driver.quit()
    return floor_cartridge_details

# Call the function and print the output
print(get_cartridge_info())
