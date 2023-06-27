import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Load the tickers from the Excel sheet
tickers_df = pd.read_excel('file.xlsx')
tickers_list = tickers_df['Ticker'].tolist()

# Function to scrape executive information from a given URL using Beautiful Soup and Selenium
def scrape_executives(url):
    # Configure Selenium webdriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

    # Path to the ChromeDriver executable
    chrome_driver_path = "/webroot/public_html/websites/odz/pythonapps/api-ticker/chromedriver"

    # Start the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # Open the URL
    driver.get(url)
    try:

        # Wait for the profile link to be visible and click it
        profile_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Profile')))
        profile_link.click()
        # if profile_link is None:
        #     worksheet.append_row([ticker, "Profile not found"])
        #     continue       

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
        print(f"Unexpected url {err=}, {type(err)=}")
        pass

# Update Google Sheet with scraped information
# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1oaeA2/edit#gid=0'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1oaeA2YoF2LX7LVkAQ2g/edit#gid=1756423001'
worksheet_name = 'Sheet3'

# Open the Google Sheet
worksheet = gc.open_by_url(spreadsheet_url).worksheet(worksheet_name)

# Iterate over each ticker and scrape executive information
for ticker in tickers_list:

    # Construct the URL for the ticker
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"    
    print(f"Start Scraping..ticker = {ticker} - pageUrl {url}")

    # Scrape the executive information for the ticker
    executives = scrape_executives(url)
    try:
        # Prepare the data to be updated in the Google Sheet
        values = []
        for executive in executives:
            if executive:
                values.append([ticker, executive['Name'], executive['Title'], executive['Pay'], executive['Exercised'], executive['Year Born']])
        
        # print(values)
        # Append the rows data in google sheet.
        if values:
            worksheet.append_rows(values)
            # worksheet.save(values)
    except Exception as err:
        print(f"Unexpected url..{url} {err=}, {type(err)=}")
        pass

print("Scraping and updating completed.")

