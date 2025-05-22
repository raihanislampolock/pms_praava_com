from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

def printer_410_details():
    floor_details = {
        "floor_nine": {
            "url": "http://10.0.2.155/hp/device/info_deviceStatus.html?tab=Home&menu=DevStatus",
            "ip": "10.0.2.155"

        }

    }

    floor_printer_details = dict()

    for key, val in floor_details.items():
        driver.get(val["url"])
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        mydiv = soup.find_all("td", {"class": "alignRight valignTop"})

        Black = (mydiv[0].get_text())
        Cyan = (mydiv[1].get_text())
        Magenta = (mydiv[2].get_text())
        Yellow = (mydiv[3].get_text())

        black = Black.replace("*", "").strip()
        cyan = Cyan.replace("*", "").strip()
        magenta = Magenta.replace("*", "").strip()
        yellow = Yellow.replace("*", "").strip()
        percent = {"black":black,"cyan":cyan,"magenta":magenta,"yellow":yellow}
        floor_printer_details[key] = {
            "ip": val["ip"],
            "percentage": percent
        }

    return floor_printer_details
