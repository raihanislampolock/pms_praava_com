from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import traceback

from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True  # Optional: run in headless mode (no UI needed in Docker)

driver = webdriver.Firefox(options=options)

def printer_508_details():
    floor_details = {
        "Floor_1_Deo_Colour": {
            "url": "https://10.1.0.247/",
            "ip": "10.1.0.247"
        },
        "Floor_3_Deo_Colour": {
            "url": "https://10.0.1.243/",
            "ip": "10.0.1.243"
        },
        "Floor_9_Corporate_Colour": {
            "url": "https://10.1.0.241/",
            "ip": "10.1.0.241"
        },
    }

    floor_printer_details = dict()

    for key, val in floor_details.items():
        try:
            driver.get(val["url"])
            wait = WebDriverWait(driver, 10)

            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")

            mydiv = soup.find_all("div", {"class": "consumable"})
            message_div = soup.find("span", {"id": "MachineStatus"})

            colours = dict()
            for div in mydiv:
                # Extract the consumable name and its percentage
                consumable_name = div.find("h2").get_text()
                percentage_span = div.find("span", {"class": "plr"})
                if percentage_span:
                    colour_percentage = percentage_span.get_text().strip("*")
                    colours[consumable_name] = colour_percentage

            floor_printer_details[key] = {
                "ip": val["ip"],
                "percentage": colours,
                "status": "online",
                "device_status": message_div.get_text() if message_div else "Unknown"
            }

        except Exception as e:
            print(f"Error occurred for {val['url']}: {str(e)}")
            print(traceback.format_exc())
            # Send data to the database with an "offline" status
            offline_data = {
                "ip": val["ip"],
                "percentage": {},
                "status": "offline",
                "device_status": ""
            }
            floor_printer_details[key] = offline_data

    return floor_printer_details

# Example usage
details = printer_508_details()
print(details)
