from flask import Flask, jsonify
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
app = Flask(__name__)

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Function to scrape executive information from a given URL using Beautiful Soup and Selenium
def scrape_executives(url):
    # Configure Selenium webdriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Path to the ChromeDriver executable
    chrome_driver_path = "./chromedriver"
    # chrome_driver_path = "./ticker_scarper/chromedriver_linux64/chromedriver"

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

# Update Google Sheet with scraped information
def update_google_sheet(ticker, executives):
    # testing google sheet
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/'
    worksheet_name = 'Sheet3'

    # Open the Google Sheet
    worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

    # Check if executives is not None
    if executives is not None:
    # Prepare the data to be updated in the Google Sheet
        values = []
        for executive in executives:
            if executive:
                values.append([ticker, executive['Name'], executive['Title'], executive['Pay'], executive['Exercised'], executive['Year Born']])
        # Append the rows data in google sheet
        if values:
            worksheet.append_rows(values)
    else:
        print(f"No executive data found for ticker: {ticker}")

@app.route('/api/<ticker>', methods=['GET'])
def get_scraped_data(ticker):
    # Construct the URL for the ticker
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"

    # Scrape the executive information for the ticker
    executives = scrape_executives(url)

    # Update Google Sheet with the scraped data
    update_google_sheet(ticker, executives)

    return jsonify({'Ticker': ticker, 'Executives': executives})

if __name__ == '__main__':
#    app.run()
    # app.run(debug=True, port=8008, host='0.0.0.0')
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))
