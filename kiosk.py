from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
import time

def wait_and_click(driver, locator, timeout=10):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    element.click()

def wait_and_send_keys(driver, locator, keys, timeout=10):
    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    element.send_keys(keys)

def perform_journey():
    GECKO_DRIVER_PATH = "C:\driver\geckodriver.exe"  # Replace with the actual path
    driver_service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=driver_service)
    url = "http://182.163.102.118:81/Feedback/Welcome.html"
    result_data = dict()

    try:
        driver.get(url)
        wait_and_click(driver, (By.XPATH, "/html/body/div[1]/div/div[2]/button[1]"))

        # Add a delay to allow the page to load
        time.sleep(2)

        wait_and_send_keys(driver, (By.NAME, "ctl00$mainContent$numSelfUPI"), "0000002393")
        wait_and_click(driver, (By.XPATH, "//*[@id='mainContent_btn_submit_screen_0']"))

        if "new-page" in driver.current_url:
            result_data['first'] = "how likely are you to recommend Praava Health! Text: Your desired text here"
        else:
            result_data['first'] = "how likely are you to recommend Praava Health! Text: Your desired text here!"

        wait_and_click(driver, (By.XPATH, "/html/body/form/div[3]/div/div[1]/div[2]/ul/li[10]/label/img"))

        if "new-page" in driver.current_url:
            result_data['second'] = "Feedback Given Successful! Text: Your desired text here"
        else:
            result_data['second'] = "Feedback Given Successful! Text: Your desired text here!"

        # Continue with the rest of your code...

        online_data ={'kiosk':{
            "ip": url,
            "percentage": result_data,
            "status": "online",
            "device_status": ""
        }}

        print(online_data)
        print("Journey Successful!")
        return online_data

    except TimeoutException:
        print("Element not found within the specified time.")

    except Exception as e:
        # If an exception occurs, print an error message
        print(f"Error: {e}")
        offline_data = {'kiosk':{
            "ip": url,
            "percentage": result_data,
            "status": "online",
            "device_status": ""
        }}
        print(offline_data)
        return offline_data

    finally:
        driver.quit()

if __name__ == "__main__":


    perform_journey()
