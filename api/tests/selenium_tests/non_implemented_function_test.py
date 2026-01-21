from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.text-green-700.text-xl"))
    )

    driver.get("https://server.tail3ce7af.ts.net/non-existing-feature")

    error_code = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//h1[normalize-space()="404"]'))
    )

    error_message = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h2[contains(normalize-space(), "Page not found")]')
        )
    )

    assert error_code.text == "404"
    assert "Page not found" in error_message.text
    assert "/login" not in driver.current_url

    print("TEST PASSED — authenticated user sees correct 404 page.")

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
