# YAHOO-finance-scarped-data
we are getting the ticker from .xlsx file and dynamic also and scrape into the google sheet.

## Get Started

1. Clone or download the project on your computer to get started. You'll need Python 3.9 or 3.10 to run this starter project as well.
2. In this project you can see there is 3 files- 
   api_ticker_scrape_save_gs.py - 
   Scrape_ticker_by_api.py -
   Scrape_ticker_from_xlsx.py - 

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
python app.py
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
python app.py
#or
export FLASK_APP=app.py
flask run
```
