from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import fnmatch

def wait_for_download(download_dir, pattern, timeout=60):
    start = time.time()
    prev_size = -1

    while time.time() - start < timeout:
        matches = [f for f in os.listdir(download_dir) if fnmatch.fnmatch(f, pattern) and not f.endswith('.crdownload')]
        if matches:
            filepath = os.path.join(download_dir, matches[0])
            size = os.path.getsize(filepath)
            if size == prev_size and size > 0:
                return True
            prev_size = size
        time.sleep(0.5)

    raise TimeoutError("Download did not complete")


options = Options()

download_dir = os.path.dirname(os.path.abspath(__file__))

prefs = {
    "download.default_directory": download_dir, 
    "download.prompt_for_download": False, 
    "directory_upgrade": True,
    "safebrowsing.enabled": True 
}
options.add_experimental_option("prefs", prefs)

driver=webdriver.Chrome(options=options)
driver.get("https://rpachallenge.com/")

if not os.path.exists(os.path.join(download_dir, "challenge.xlsx")):
    driver.find_element(By.CSS_SELECTOR, 'a[href*="challenge.xlsx"]').click()
    wait_for_download(download_dir, "*challenge.xlsx")


data=pd.read_excel(os.path.join(download_dir, "challenge.xlsx"))
print(data)

button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
button.click()

data.columns = data.columns.str.strip()
for row in data.iterrows():
    form_fields=driver.find_elements(By.TAG_NAME,"rpa1-field")
    for field in form_fields:
        name=field.find_element(By.TAG_NAME, "label").text
        print(row[1][name])
        input=field.find_element(By.TAG_NAME,"input")
        input.clear()
        input.send_keys(row[1][name])
    driver.find_element(By.TAG_NAME, "form").find_element("xpath", "//input[@class='btn uiColorButton']").click()



result=driver.find_element(By.CLASS_NAME,"message2").text
print(result)

driver.quit()
