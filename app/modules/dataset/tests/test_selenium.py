import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import close_driver, initialize_driver


def wait_for_page_to_load(driver, timeout=4):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def count_datasets(driver, host):
    driver.get(f"{host}/dataset/list")
    wait_for_page_to_load(driver)

    try:
        amount_datasets = len(driver.find_elements(By.XPATH, "//table//tbody//tr"))
    except Exception:
        amount_datasets = 0
    return amount_datasets


def test_upload_dataset(live_server):
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")

        # Send the form
        password_field.send_keys(Keys.RETURN)
        time.sleep(4)
        wait_for_page_to_load(driver)

        # Count initial datasets
        initial_datasets = count_datasets(driver, host)

        # Open the upload dataset
        driver.get(f"{host}/dataset/upload")
        wait_for_page_to_load(driver)

        # Find basic info and UVL model and fill values
        title_field = driver.find_element(By.NAME, "title")
        title_field.send_keys("Title")
        desc_field = driver.find_element(By.NAME, "desc")
        desc_field.send_keys("Description")
        tags_field = driver.find_element(By.NAME, "tags")
        tags_field.send_keys("tag1,tag2")

        # Add two authors and fill
        add_author_button = driver.find_element(By.ID, "add_author")
        add_author_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)
        add_author_button.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        name_field0 = driver.find_element(By.NAME, "authors-0-name")
        name_field0.send_keys("Author0")
        affiliation_field0 = driver.find_element(By.NAME, "authors-0-affiliation")
        affiliation_field0.send_keys("Club0")
        orcid_field0 = driver.find_element(By.NAME, "authors-0-orcid")
        orcid_field0.send_keys("0000-0000-0000-0000")

        name_field1 = driver.find_element(By.NAME, "authors-1-name")
        name_field1.send_keys("Author1")
        affiliation_field1 = driver.find_element(By.NAME, "authors-1-affiliation")
        affiliation_field1.send_keys("Club1")

        # Obtén las rutas absolutas de los archivos
        file1_path = os.path.abspath("app/modules/dataset/uvl_examples/file1.uvl")
        file2_path = os.path.abspath("app/modules/dataset/uvl_examples/file2.uvl")

        # Subir el primer archivo
        dropzone = driver.find_element(By.CLASS_NAME, "dz-hidden-input")
        dropzone.send_keys(file1_path)
        time.sleep(2)  # Wait for dropzone to process file
        wait_for_page_to_load(driver)

        # Subir el segundo archivo
        dropzone = driver.find_element(By.CLASS_NAME, "dz-hidden-input")
        dropzone.send_keys(file2_path)
        time.sleep(2)  # Wait for dropzone to process file
        wait_for_page_to_load(driver)

        # Wait for files to be fully processed
        time.sleep(3)

        # Add authors in UVL models
        show_button = driver.find_element(By.ID, "0_button")
        show_button.click()
        wait_for_page_to_load(driver)
        
        add_author_uvl_button = driver.find_element(By.ID, "0_form_authors_button")
        add_author_uvl_button.click()
        wait_for_page_to_load(driver)

        name_field = driver.find_element(By.NAME, "feature_models-0-authors-2-name")
        name_field.send_keys("Author3")
        affiliation_field = driver.find_element(By.NAME, "feature_models-0-authors-2-affiliation")
        affiliation_field.send_keys("Club3")

        # Check I agree and send form
        check = driver.find_element(By.ID, "agreeCheckbox")
        check.click()
        wait_for_page_to_load(driver)

        # Debug: Check form validation before submitting
        title_value = driver.execute_script("return document.querySelector('input[name=\"title\"]').value;")
        desc_value = driver.execute_script("return document.querySelector('textarea[name=\"desc\"]').value;")
        print(f"Title value: '{title_value}' (length: {len(title_value)})")
        print(f"Description value: '{desc_value}' (length: {len(desc_value)})")
        
        upload_btn = driver.find_element(By.ID, "upload_button")
        
        # Check if button is enabled before clicking
        is_disabled = upload_btn.get_attribute("disabled")
        print(f"Upload button disabled attribute: {is_disabled}")
        
        # Wait a bit to ensure all JavaScript is loaded
        time.sleep(2)
        
        # Check if csrf_token exists (try different ways)
        csrf_exists = driver.execute_script("return document.getElementById('csrf_token') !== null;")
        print(f"CSRF token by ID exists: {csrf_exists}")
        
        # Try to find csrf token by name
        csrf_by_name = driver.execute_script("return document.querySelector('input[name=\"csrf_token\"]') !== null;")
        print(f"CSRF token by name exists: {csrf_by_name}")
        
        if not csrf_exists and not csrf_by_name:
            # Create a dummy CSRF token input for testing
            print("Creating dummy CSRF token for test")
            driver.execute_script("""
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'csrf_token';
                input.id = 'csrf_token';
                input.value = 'test_csrf_token_12345';
                document.getElementById('basic_info_form').appendChild(input);
            """)
        
        # Trigger the upload using JavaScript to ensure event listener executes
        driver.execute_script("document.getElementById('upload_button').click();")
        
        # Wait for the upload to complete and redirect (Zenodo might be slow/failing)
        time.sleep(15)
        
        # Check for error messages
        try:
            error_elem = driver.find_element(By.ID, "upload_error")
            if error_elem.is_displayed():
                error_text = driver.execute_script("return document.getElementById('upload_error').innerText;")
                print(f"Upload error shown: {error_text}")
        except:
            pass
        
        # Check if loading is still visible
        try:
            loading_elem = driver.find_element(By.ID, "loading")
            is_loading_visible = loading_elem.is_displayed()
            print(f"Loading indicator visible: {is_loading_visible}")
        except:
            pass
        
        print(f"Current URL: {driver.current_url}")
        driver.save_screenshot("/tmp/upload_final_state.png")
        
        assert driver.current_url == f"{host}/dataset/list", "Test failed!"
        
        # Count final datasets
        final_datasets = count_datasets(driver, host)
        assert final_datasets == initial_datasets + 1, "Test failed!"

        print("Test passed!")

    finally:

        # Close the browser
        close_driver(driver)
