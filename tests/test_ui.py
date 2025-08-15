import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE = 'http://localhost:5000'

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    drv = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    yield drv
    drv.quit()

def test_ui_apply_form(driver):
    driver.get(BASE)
    time.sleep(0.5)
    driver.find_element(By.NAME, 'name').send_keys('Guy')
    driver.find_element(By.NAME, 'email').send_keys('guy@example.com')
    driver.find_element(By.NAME, 'phone').send_keys('0501234567')
    sel = driver.find_element(By.NAME, 'position')
    for opt in sel.find_elements(By.TAG_NAME, 'option'):
        if opt.get_attribute('value') == 'Software Engineer': opt.click(); break
    resume_path = os.path.join(os.path.dirname(__file__), 'dummy_resume.pdf')
    with open(resume_path, 'wb') as f: f.write(b'%PDF-1.4\n% Dummy')
    driver.find_element(By.NAME, 'resume').send_keys(resume_path)
    driver.find_element(By.NAME, 'accept').click()
    driver.find_element(By.XPATH, "//button[text()='Submit Application']").click()
    time.sleep(0.5)
    body = driver.find_element(By.TAG_NAME, 'body').text
    assert 'Form submitted successfully!' in body
    os.remove(resume_path)