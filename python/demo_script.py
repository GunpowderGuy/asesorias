from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the web driver (Make sure ChromeDriver is installed and in your PATH)
driver = webdriver.Chrome()

# Define a function to take screenshots
def take_screenshot(step_name):
    driver.save_screenshot(f"{step_name}.png")

# 1. Open the Web App
driver.get("http://127.0.0.1:5000")  # Change to the URL where Flask is running
take_screenshot("01_homepage")

# 2. Register as a Tutor with Validation
driver.find_element(By.LINK_TEXT, "Crear una cuenta").click()
time.sleep(1)  # Wait for page to load
driver.find_element(By.NAME, "email").send_keys("tutor@edu.pe")
driver.find_element(By.NAME, "password").send_keys("password123")
driver.find_element(By.NAME, "role").send_keys("tutor")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
take_screenshot("02_register_tutor")

# 3. Register as a Student
driver.find_element(By.LINK_TEXT, "Crear una cuenta").click()
time.sleep(1)
driver.find_element(By.NAME, "email").send_keys("student@domain.com")
driver.find_element(By.NAME, "password").send_keys("password123")
driver.find_element(By.NAME, "role").send_keys("student")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
take_screenshot("03_register_student")

# 4. Log in as Student
driver.get("http://127.0.0.1:5000/login")
driver.find_element(By.NAME, "email").send_keys("student@domain.com")
driver.find_element(By.NAME, "password").send_keys("password123")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
take_screenshot("04_student_dashboard")

# 5. Search for Tutors
driver.find_element(By.LINK_TEXT, "Buscar Asesores").click()
time.sleep(1)
driver.find_element(By.NAME, "subject").send_keys("Matemáticas")
driver.find_element(By.NAME, "city").send_keys("Lima")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
take_screenshot("05_search_tutors")

# 6. Schedule a Session with a Tutor
schedule_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//form//button[@type='submit']"))
)
schedule_button.click()
driver.find_element(By.NAME, "date").send_keys("2024-10-10")
take_screenshot("06_schedule_tutoring")

# 7. Log out
driver.find_element(By.LINK_TEXT, "Logout").click()
take_screenshot("07_logout")

# Close the driver
driver.quit()
