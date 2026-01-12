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

    email_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_input.send_keys("test@test.com")

    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_input.send_keys("test")

    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]'))
    )
    login_button.click()

    welcome_header = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'h2.text-green-700.text-xl')
        )
    )

    search_box = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//div[contains(@class, "cursor-text") and contains(., "Search")]'
            )
        )
    )
    search_box.click()

    search_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[type="search"][placeholder="Search"]')
        )
    )
    search_input.clear()
    search_input.send_keys("non-existing activity")

    not_found_header = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h2[normalize-space()="Not found..."]')
        )
    )

    assert not_found_header.is_displayed(), "Not found message was not displayed"

    print("TEST PASSED — 'Not found...' message appeared after search.")

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
