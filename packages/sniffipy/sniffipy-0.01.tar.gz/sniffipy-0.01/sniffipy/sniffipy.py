from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import geckodriver_autoinstaller


def webdriver_generate():
    geckodriver_autoinstaller.install()
    profile = webdriver.FirefoxProfile()
    options = Options()
    options.headless = True
    profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile, options=options)


def sniffer_data(id):
    tmp = ""
    ip = []
    date = []
    ua = []
    driver = webdriver_generate()
    driver.get('https://sniffip.com/en/dashboard/' + id)
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, "text-success")))
    for row in driver.find_elements_by_class_name("odd"):
        if 'available in table' not in row.text.replace("Ports beta Map", "")[::-1][:18][::-1]:
            date.append(row.text.replace("Ports beta Map", "")[::-1][:18][::-1].replace('available in table', ""))
        for char in row.text:
            if char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6" or char == "7" or char == "8" or char == "9" or char == "0" or char == ".":
                tmp = tmp + char
            else:
                break
        if tmp != "":
            ip.append(tmp)
            ua.append(row.text.replace(date[len(date) - 1], "").replace(tmp, "").replace("Ports beta Map", ""))
            tmp = ""

    for row in driver.find_elements_by_class_name("even"):
        if 'available in table' not in row.text.replace("Ports beta Map", "")[::-1][:18][::-1]:
            date.append(row.text.replace("Ports beta Map", "")[::-1][:18][::-1])
        for char in row.text:
            if char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6" or char == "7" or char == "8" or char == "9" or char == "0" or char == ".":
                tmp = tmp + char
            else:
                break
        if tmp != "":
            ip.append(tmp)
            ua.append(row.text.replace(date[len(date) - 1], "").replace(tmp, ""))
            tmp = ""
    driver.quit()
    return {"ip": ip, "useragent": ua, "date": date}


def create_sniffer(url):
    driver = webdriver_generate()
    driver.get('https://sniffip.com')
    driver.find_element_by_class_name("input_url").click()
    driver.find_element_by_class_name("input_url").send_keys(url)
    driver.find_element_by_class_name("btn-lg").click()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, "text-success")))
    trackingId = driver.find_element_by_class_name("text-success").text
    targetUrl = driver.find_element_by_class_name("short_link").text
    driver.quit()
    return {'trackingId': trackingId, 'url': targetUrl}

