# YAHOO-finance-scarped-data
we are getting the ticker from .xlsx file and dynamic also and scrape into the google sheet.

## Get Started

1. Clone or download the project on your computer to get started. You'll need Python 3.9 or 3.10 to run this starter project as well.
2. In this project you can see there is 3 files- 

   ## api_ticker_scrape_save_gs.py - 
     
      This file scrape all the tickers through api(localhost:4444/api/ticker 'enter') and save it in googlespreadsheet

   ## Scrape_ticker_by_api.py - 
     
      This file scarpe ticker through api-(localhost:4444/api/ticker 'enter') while if we pass the ticker into api and return the json response in the browser.

   ## Scrape_ticker_from_xlsx.py - 
     
      In this file we can scrape ticker and load from the xlsx file and scrape it all and save it into the googlespreadsheet and as well as return the son response in the browser.

   ## XLSX - xlsx file contanis the name of the ticker. 

#### Windows

3. **Create and activate a virtual environment**
```python
python -m venv .venv
.venv\Scripts\activate
```

4. **Install dependencies**  
```python
python3 -m pip install --upgrade pip && pip3 install -r requirements.txt
```

5. **Run the server locally**  
```python
python <filename.py>
```

#### macOS/ Linux

3. **Create and activate a virtual environment**
```python
python -m venv .venv
source .venv/bin/activate
```

**or **

```python
sudo apt-get install -y python3.10-venv
python3.10 -m venv <name og the env: .venv >
source .venv/bin/activate
```

4. **Install dependencies**
```python
python3 -m pip install --upgrade pip && pip3 install -r requirements.txt
```

5. **Run the server**
```python
python <filename.py>
#or
export FLASK_APP=app.py
flask run
```
