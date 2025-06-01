import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import traceback

def get_cartridge_info():
    # Define the floor details
    floor_details = {
        "Floor_1_Pharmacy_Black": {
            "url": "http://10.1.0.249/login.html",
            "ip": "10.1.0.249",
            "cartridge_xpath": "//div[@class='table_row']//td[2]//span[2]"
        },
    }

    floor_cartridge_details = {}

    # Loop through each printer
    for key, val in floor_details.items():
        options = Options()
        options.headless = True

        driver = None
        try:
            # Create a fresh driver for this printer
            driver = webdriver.Firefox(options=options)

            driver.get(val["url"])
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitButton"]')))
            element.click()

            # Get page content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            toner_section = soup.find('div', {'id': 'tonerInfomationModule'})
            td_elements = toner_section.findChildren("td")

            if not td_elements:
                raise ValueError("No <td> found under tonerInfomationModule")

            cartridge_level = td_elements[0].text
            number = re.findall(r'\d+', cartridge_level)[0]  # Extract percentage number

            # Get status message
            status_message_div = soup.find("span", {"class": "StatusMessage"})
            span_text = status_message_div.text.strip() if status_message_div else "Unknown"

            # Store info
            percent = {"black": number}
            floor_cartridge_details[key] = {
                "ip": val["ip"],
                "percentage": percent,
                "status": "online",
                "device_status": span_text
            }

        except Exception as e:
            print(f"Error retrieving cartridge info for {key}: {str(e)}")
            print(traceback.format_exc())
            floor_cartridge_details[key] = {
                "ip": val["ip"],
                "percentage": {},
                "status": "offline",
                "device_status": "Offline"
            }

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    return floor_cartridge_details

# Run the function
if __name__ == "__main__":
    result = get_cartridge_info()
    print(result)
