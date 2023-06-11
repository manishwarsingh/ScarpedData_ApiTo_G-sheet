from flask import Flask, jsonify
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
app = Flask(__name__)

# Function to scrape executive information from a given URL using Beautiful Soup and Selenium
def scrape_executives(url):
    # Configure Selenium webdriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Path to the ChromeDriver executable
    # chrome_driver_path = "/webroot/public_html/websites/odz/pythonapps/api-ticker/chromedriver"
    chrome_driver_path = "./ticker_scarper/chromedriver_linux64/chromedriver"

    # Start the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # Open the URL
    driver.get(url)
    time.sleep(5)
    try:
        # Wait for the profile link to be visible and click it
        profile_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Profile')))
        profile_link.click()

        # Wait for the profile page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Main"]')))

        # Get the page source
        page_source = driver.page_source

        # Close the browser
        driver.quit()

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, 'html.parser')

        executives = []
        executive_table = soup.find('table', {'class': 'W(100%)'})
        if executive_table:
            rows = executive_table.find_all('tr')
            for row in rows[1:]:
                cells = row.find_all('td')
                name = cells[0].text.strip()
                title = cells[1].text.strip()
                pay = cells[2].text.strip()
                exercised = cells[3].text.strip()
                year_born = cells[4].text.strip()
                executives.append({'Name': name, 'Title': title, 'Pay': pay, 'Exercised': exercised, 'Year Born': year_born})

        return executives
    except Exception as err:
        print(f"Unexpected error {err=}, {type(err)=}")
        pass

@app.route('/api/<ticker>', methods=['GET'])
def get_scraped_data(ticker):
    # Construct the URL for the ticker
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"

    # Scrape the executive information for the ticker
    executives = scrape_executives(url)    

    return jsonify({'Ticker': ticker, 'Executives': executives})

if __name__ == '__main__':
#    app.run()
    # app.run(debug=True, port=8008, host='0.0.0.0')
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
