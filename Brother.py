from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import traceback

def printer_brother_details():
    floor_details = {
        "Floor_1_Fde": {"url": "http://10.1.0.248/general/status.html", "ip": "10.1.0.248"},
        "Floor_2_Fde": {"url": "http://10.1.0.250/general/status.html", "ip": "10.1.0.250"},
        "Floor_2_Nurse": {"url": "http://10.1.0.251/general/status.html", "ip": "10.1.0.251"},
        "Floor_3_Fde": {"url": "http://10.0.2.145/general/status.html", "ip": "10.0.2.145"},
        "Floor_3_Deo": {"url": "http://10.0.0.226/general/status.html", "ip": "10.0.0.226"},
        "Floor_4_Fde": {"url": "http://10.1.0.243/general/status.html", "ip": "10.1.0.243"},
        "Floor_5_Fde": {"url": "http://10.1.0.246/general/status.html", "ip": "10.1.0.246"},
        "Floor_6_Fde": {"url": "http://10.0.4.171/general/status.html", "ip": "10.0.4.171"},
        "Floor_7_Lab": {"url": "http://10.0.1.209/general/status.html", "ip": "10.0.1.209"},
        "Floor_8_Lab": {"url": "http://10.0.4.134/general/status.html", "ip": "10.0.4.134"},
        "Floor_8_Corporate": {"url": "http://10.1.0.242/general/status.html", "ip": "10.1.0.242"},
        "Floor_9_Corporate": {"url": "http://10.1.0.240/general/status.html", "ip": "10.1.0.240"}
    }

    floor_printer_details = {}

    for key, val in floor_details.items():
        offline_data = {
            "ip": val["ip"],
            "percentage": {},
            "status": "offline",
            "device_status": "Offline"
        }

        try:
            # Create a new driver for each request
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)

            driver.get(val["url"])
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tonerremain"))
            )

            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")

            toner_img = soup.find("img", {"class": "tonerremain"})
            status_spans = soup.find_all("span", {"class": "moni moniOk"})

            height = int(toner_img['height'])
            perc = int((height / 56) * 100)

            span_text = status_spans[0].text if status_spans else "Unknown"

            floor_printer_details[key] = {
                "ip": val["ip"],
                "percentage": {"black": perc},
                "status": "online",
                "device_status": span_text
            }

        except Exception as e:
            print(f"Error occurred for {val['url']}: {str(e)}")
            print(traceback.format_exc())
            floor_printer_details[key] = offline_data

        finally:
            # Always close driver for each printer
            try:
                driver.quit()
            except:
                pass

    return floor_printer_details

# Run the function
if __name__ == "__main__":
    result = printer_brother_details()
    print(result)
