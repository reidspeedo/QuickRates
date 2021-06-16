from selenium import webdriver
from chromedriver_py import binary_path
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
import random

path = r"/Users/reidrelatores/PycharmProjects/farmers/chromedriver"
url = "https://www.nerdwallet.com/article/insurance/estimate-home-insurance"



def start_chrome(url):
    # Initialize Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--log-level=3")
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    driver.get(url)
    return driver

def filter_zips(file, state="Washington"):
    az = pd.read_csv(file, usecols=['zip', 'state_name'])
    state_zips = az[az['state_name'] == state]['zip']
    return state_zips

def scrape_process(driver, state, state_zips, wait):
    input('start?')
    driver.switch_to.frame('iFrameResizer1')
    driver.find_element(By.XPATH, f"//*[@vt='{state}']").click()
    premiums = []

    for zip in state_zips:
        zip_input = driver.find_element(By.XPATH, "//*[@id='fieldname29_1']")
        zip_input.clear()
        zip_input.send_keys(str(zip))
        sleep(2)
        premium = driver.find_element(By.XPATH, "//*[@id='fieldname25_1']").get_attribute('value')
        premiums.append(premium)
        print(zip, premium, state)
        sleep(2)

    data = {'zip': state_zips,
            'premium': premiums,
            'state': [state]*len(state_zips)}

    zip_df = pd.DataFrame(data, columns=['zip', 'premium', 'state'])
    return zip_df





if __name__ == '__main__':
    state = "Washington"
    url = "https://www.nerdwallet.com/article/insurance/estimate-home-insurance"
    uszipcodes = r"/Users/reidrelatores/PycharmProjects/QuickRate/nerdwallet_scraper/uszips.csv"
    driver = start_chrome(url)
    state_zips = filter_zips(uszipcodes)
    zip_df = scrape_process(driver, state, state_zips, 4)
    zip_df.to_csv('zip_avg_premium.csv', mode='a', header=True, index=False)