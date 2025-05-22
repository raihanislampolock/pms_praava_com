from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService, Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import traceback

GECKO_DRIVER_PATH = "C:\\driver\\geckodriver.exe"  # Replace with the actual path

# Create a Service object
service = Service(executable_path=GECKO_DRIVER_PATH)

# Create a Firefox driver instance with the Service object
driver = webdriver.Firefox(service=service)


def printer_230_details():
    floor_details = {
        "Floor_1_Pharmacy": {
            "url": "http://10.1.0.249/hp/device/info_deviceStatus.html?tab=Home&menu=DevStatus",
            "ip": "10.1.0.249"
        }
    }

    floor_printer_details = {}

    try:
        # Create a Service object
        service = FirefoxService(executable_path=GECKO_DRIVER_PATH)

        # Create Firefox options
        firefox_options = FirefoxOptions()

        # Set headless mode if desired
        firefox_options.headless = True  # Set to False if you want to see Firefox UI

        for key, val in floor_details.items():
            offline_data = {
                "ip": val["ip"],
                "percentage": {},
                "status": "offline",
                "device_status": "Offline"
            }

            try:
                # Create Firefox driver instance with the Service object and options
                driver = webdriver.Firefox(service=service, options=firefox_options)

                driver.get(val["url"])
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.alignRight.valignTop')))

                content = driver.page_source
                soup = BeautifulSoup(content, 'html.parser')
                mydiv = soup.find_all("td", {"class": "alignRight valignTop"})
                mydiv2 = soup.find_all("td", {"class": "itemLargeFont"})
                Black = mydiv[0].get_text().replace("†", "").replace("%", "").strip()
                Drum = mydiv[1].get_text().replace("†", "").replace("%", "").strip()
                percent = {"black": Black, "drum": Drum}
                td_text = mydiv2[0].text.strip()

                floor_printer_details[key] = {
                    "ip": val["ip"],
                    "percentage": percent,
                    "status": "online",
                    "device_status": td_text
                }

                driver.quit()  # Close WebDriver session after use

            except TimeoutException:
                print(f"Timeout occurred for {val['url']}")
                floor_printer_details[key] = offline_data

            except Exception as e:
                print(f"Error occurred for {val['url']}: {str(e)}")
                print(traceback.format_exc())
                floor_printer_details[key] = offline_data

    except Exception as e:
        print(f"Error initializing Firefox WebDriver: {str(e)}")
        print(traceback.format_exc())

    return floor_printer_details


print(printer_230_details())
