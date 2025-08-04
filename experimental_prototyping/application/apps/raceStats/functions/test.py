from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time






# import shutil
# import os
# import subprocess

# original_profile = r"C:\Users\\AppData\Local\Google\Chrome\User Data\Profile 2"
# selenium_profile = r"C:\Users\\AppData\Local\Google\Chrome\SeleniumProfile"

# if os.path.exists(selenium_profile):
#     print("✅ Selenium profile already exists.")
# else:
#     print("🔁 Copying Chrome profile...")
#     shutil.copytree(original_profile, selenium_profile)
#     print("✅ Done copying profile.")

# # Launch Chrome with new profile
# chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# launch_cmd = f'"{chrome_path}" --user-data-dir="{selenium_profile}"'

# print("🚀 Launching Chrome with SeleniumProfile...")
# subprocess.Popen(launch_cmd)







# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# profile_path = r"C:\Users\\AppData\Local\Google\Chrome\SeleniumProfile"

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# profile_path = r"C:\Users\\AppData\Local\Google\Chrome\SeleniumFreshProfile"

# options = Options()
# options.add_argument(f"user-data-dir={profile_path}")

# driver = webdriver.Chrome(options=options)
# driver.get("https://www.google.com")

# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))


