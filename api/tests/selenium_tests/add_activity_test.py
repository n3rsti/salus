from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://server.tail3ce7af.ts.net/login")

    try:
        agree_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='I agree']"
                )
            )
        )
        agree_button.click()
        print("INFO — Cookie consent accepted.")
    except TimeoutException:
        print("INFO — Cookie consent not present, continuing.")

    email_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_input.send_keys("test@test.com")

    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_input.send_keys("test")

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
        )
    )
    login_button.click()

    activity_span = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//div[@data-sidebar="content"]//span[normalize-space()="Activities"]',
            )
        )
    )

    activity_span.click()

    create_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Create"]'))
    )

    create_button.click()

    name_input = wait.until(EC.presence_of_element_located((By.ID, "name")))
    name_input.clear()
    name_input.send_keys("Morning Cardio")

    description_textarea = wait.until(
        EC.presence_of_element_located((By.ID, "description"))
    )
    description_textarea.clear()
    description_textarea.send_keys("Light cardio workout to start the day.")

    content_textarea = wait.until(
        EC.presence_of_element_located((By.ID, "content"))
    )
    content_textarea.clear()
    content_textarea.send_keys("Follow these steps!")

    duration_input = wait.until(EC.presence_of_element_located((By.ID, "duration")))
    duration_input.clear()
    duration_input.send_keys("30")

    file_path = Path(__file__).parent / "test_image.jpg"

    image_input = wait.until(EC.presence_of_element_located((By.ID, "image")))
    image_input.send_keys(str(file_path.resolve()))

    moderate_radio = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[@role="radio" and @id="moderate"]')
        )
    )
    moderate_radio.click()

    submit_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[@type="submit" and normalize-space()="Submit"]')
        )
    )

    submit_button.click()

    activity_name = "Morning Cardio"

    activity_header = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h1[contains(@class, "font-bold")]')
        )
    )

    header_text = activity_header.text

    assert activity_name in header_text, (
        f"TEST FAILED. Expected activity name '{activity_name}', "
        f"but got header text: '{header_text}'"
    )

    print(f"TEST PASSED — activity '{activity_name}' was successfully created.")

except TimeoutException as e:
    print("TEST FAILED — one of the expected elements did not appear in time.")
    print(f"Details: {e}")

except AssertionError as e:
    print(f"TEST FAILED — assertion error: {e}")

except Exception as e:
    print("TEST FAILED — unexpected error occurred.")
    print(f"Details: {e}")

finally:
    driver.quit()
