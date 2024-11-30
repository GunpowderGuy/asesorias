from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# Variable to control the speed of the script for debugging
DEBUG_DELAY = 1  # Adjust this value to make the script slower or faster

# Set up the WebDriver
driver = webdriver.Chrome()

# Function to control the delay based on DEBUG_DELAY
def debug_sleep():
    time.sleep(DEBUG_DELAY)

# Screenshot function
def take_screenshot(step_name):
    driver.save_screenshot(f"{step_name}.png")
    debug_sleep()

# Helper function to click a link with retries
def click_link_with_retries(text, retries=3):
    for _ in range(retries):
        try:
            link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, text))
            )
            link.click()
            debug_sleep()
            return True
        except Exception as e:
            print(f"Retrying to find the link '{text}': {e}")
            debug_sleep()
    print(f"Failed to find the link '{text}' after {retries} attempts.")
    return False

# Step 1: Open the Web App
driver.get("http://127.0.0.1:5000")
take_screenshot("01_homepage")

# Step 2: Register a Tutor
if click_link_with_retries("Crear una cuenta"):
    try:
        debug_sleep()
        driver.find_element(By.NAME, "email").send_keys("tutor@edu.pe")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.ID, "role").send_keys("tutor")

        # Tutor-specific fields
        driver.find_element(By.NAME, "courses").send_keys("Matemáticas, Física")
        driver.find_element(By.NAME, "availability_day").send_keys("Lunes")
        
        # Set time fields using JavaScript to bypass AM/PM issues
        start_time_script = "document.getElementsByName('availability_start')[0].value = '10:00 AM';"
        end_time_script = "document.getElementsByName('availability_end')[0].value = '12:00 PM';"
        driver.execute_script(start_time_script)
        driver.execute_script(end_time_script)

        take_screenshot("02_register_tutor_before_submit")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        take_screenshot("03_register_tutor_after_submit")
    except Exception as e:
        print(f"Error during tutor registration: {e}")
        driver.quit()

# Step 3: Register a Student
if click_link_with_retries("Crear una cuenta"):
    try:
        debug_sleep()
        driver.find_element(By.NAME, "email").send_keys("student@domain.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.ID, "role").send_keys("student")
        take_screenshot("04_register_student_before_submit")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        take_screenshot("05_register_student_after_submit")
    except Exception as e:
        print(f"Error during student registration: {e}")
        driver.quit()

# Step 4: Log in as Student
try:
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "email").send_keys("student@domain.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    take_screenshot("06_student_dashboard")
except Exception as e:
    print(f"Error during student login: {e}")
    driver.quit()

# Step 5: Search for Tutors as Student
try:
    if click_link_with_retries("Buscar más asesores"):
        driver.find_element(By.NAME, "subject").send_keys("Matemáticas")
        driver.find_element(By.NAME, "city").send_keys("Lima")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        take_screenshot("07_search_tutors_results")
except Exception as e:
    print(f"Error during tutor search: {e}")
    driver.quit()

# Step 6: Schedule a Tutoring Session with a Tutor (using a future date)
try:
    # Select a future date for scheduling (e.g., 7 days from now)
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    schedule_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form//button[@type='submit']"))
    )
    schedule_button.click()
    
    # Set the date and time for the tutoring session
    driver.find_element(By.NAME, "date").send_keys(f"Lunes {future_date} 10:00 - 12:00")
    take_screenshot("08_schedule_tutoring")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    debug_sleep()
except Exception as e:
    print(f"Error during session scheduling: {e}")
    driver.quit()

# Step 7: Check Student Dashboard for Scheduled Sessions
try:
    driver.get("http://127.0.0.1:5000/dashboard")
    take_screenshot("09_student_dashboard_with_scheduled_sessions")
    
    # Verify if the session appears in upcoming sessions
    upcoming_sessions = driver.find_elements(By.XPATH, "//ul[contains(@class, 'upcoming-sessions')]/li")
    session_found = any(future_date in session.text for session in upcoming_sessions)
    if session_found:
        print("The scheduled session was successfully found in the upcoming sessions.")
    else:
        print("The scheduled session was not found in the upcoming sessions.")
except Exception as e:
    print(f"Error checking student dashboard: {e}")
    driver.quit()

# Step 8: Log out as Student
if click_link_with_retries("Logout"):
    take_screenshot("10_student_logout")

# Step 9: Log in as Tutor to Verify Scheduled Session
try:
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "email").send_keys("tutor@edu.pe")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    take_screenshot("11_tutor_dashboard")
except Exception as e:
    print(f"Error during tutor login: {e}")
    driver.quit()

# Close the WebDriver
driver.quit()

