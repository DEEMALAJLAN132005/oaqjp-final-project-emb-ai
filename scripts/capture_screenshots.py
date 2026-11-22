"""Capture actual Flask browser screenshots for the graded assessment."""

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

OUT = Path("evidence")
OUT.mkdir(exist_ok=True)
options = Options()
for arg in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
            "--window-size=1280,900"):
    options.add_argument(arg)
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://127.0.0.1:" + os.environ.get("PORT", "5000"))
    WebDriverWait(driver, 15).until(
        lambda browser: browser.find_element(By.ID, "analyzeButton")
    )
    driver.save_screenshot(str(OUT / "6b_deployment_test.png"))
    driver.find_element(By.ID, "analyzeButton").click()
    WebDriverWait(driver, 15).until(
        lambda browser: "Invalid text! Please try again!" in
        browser.find_element(By.ID, "system_response").text
    )
    driver.save_screenshot(str(OUT / "7c_error_handling_interface.png"))
    print("Captured actual deployment and blank-input UI screenshots.")
finally:
    driver.quit()
