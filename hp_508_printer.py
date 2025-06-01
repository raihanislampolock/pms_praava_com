from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import traceback
from selenium.webdriver.firefox.options import Options

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
        options = Options()
        options.headless = True

        driver = None
        try:
            driver = webdriver.Firefox(options=options)

            driver.get(val["url"])
            wait = WebDriverWait(driver, 10)
            
            # Optional: wait for something specific if needed, e.g.:
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "consumable")))

            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")

            mydiv = soup.find_all("div", {"class": "consumable"})
            message_div = soup.find("span", {"id": "MachineStatus"})

            colours = {}
            for div in mydiv:
                consumable_name = div.find("h2").get_text() if div.find("h2") else "Unknown"
                percentage_span = div.find("span", {"class": "plr"})
                colour_percentage = percentage_span.get_text().strip("*") if percentage_span else "Unknown"
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
            floor_printer_details[key] = {
                "ip": val["ip"],
                "percentage": {},
                "status": "offline",
                "device_status": ""
            }
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    return floor_printer_details


if __name__ == "__main__":
    result = printer_508_details()
    print(result)
