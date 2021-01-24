import unittest
import time
from selenium import webdriver

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver")
        self.driver.get("http://localhost:5000/form")

    def tearDown(self):
        self.driver.quit()

    def test_browser_title_contains_app_name(self):
        self.assertIn("Assessment", self.driver.title)

    def test_page_heading_is_datepicker_form(self):
        heading = self.driver.find_elements_by_id("heading")
        heading = heading[0].text
        self.assertEqual(heading, "Datepicker Form")

    def test_page_contains_form(self):
        form_elem = self.driver.find_elements_by_id("date-form")
        self.assertIsNotNone(form_elem)

    def test_page_contains_date_bar(self):
        form_elem = self.driver.find_elements_by_id("datebar")
        self.assertIsNotNone(form_elem)

    def test_page_contains_submit_button(self):
        form_elem = self.driver.find_elements_by_id("submit-button")
        self.assertIsNotNone(form_elem)

    def test_input_to_date_bar_press_submit_displays_json(self):
        self.driver.find_element_by_xpath("//*[@id='datebar']").send_keys("01/08/2019")
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/form/input[2]").click()
        time.sleep(3)
        json_obj = self.driver.find_element_by_xpath("/html/body/pre")
        self.assertIsNotNone(json_obj)

if __name__ == "__main__":
    unittest.main()
