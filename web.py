import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

def check_500_errors(urls):
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code >= 400:
                print(f"The URL {url} is causing a {response.status_code} error.")
        except Exception as e:
            print(f"An error occurred while checking {url}: {e}")

def perform_selenium_actions(url_xpath_mapping):
    firefox_options = Options()
    firefox_options.add_argument("--detach")
    driver = webdriver.Firefox(options=firefox_options)
    url_results = dict()

    for url, xpath in url_xpath_mapping.items():
        driver.get(url)
        time.sleep(3)

        try:
            title_element = driver.find_element(By.XPATH, xpath)
            title_text = title_element.text.strip()

            if title_text:
                url_results[url] = title_text;
                print(f"The URL {url} is working. Title: {title_text}")
            else:
                url_results[url] = 'not found';
                print(f"The URL {url} is working. Title is not available.")
        except Exception as e:
            print(f"The URL {url} is broken or down. Error: {e}")

    print(url_results)
    online_data = {'Website': {
        "ip": 'www.praavahealth.com',
        "percentage": url_results,
        "status": "online",
        "device_status": ""
    }}

    driver.quit()
    return online_data;

if __name__ == "__main__":
    urls_to_check = [
        "https://www.praavahealth.com/praava-services/",
        "https://www.praavahealth.com/praava-services/our-doctors/",
        "https://www.praavahealth.com/about/",
        "https://www.praavahealth.com/community/blog/",
        "https://www.praavahealth.com/community/events/",
        "https://www.praavahealth.com/community/press/",
        "https://www.praavahealth.com/community/gallery/",
        "https://www.praavahealth.com/contact/",
    ]

    check_500_errors(urls_to_check)
