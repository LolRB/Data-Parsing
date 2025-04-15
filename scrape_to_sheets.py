import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Scrape data from a web page
url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract article titles
titles = [item.get_text() for item in soup.select(".titleline a")]

# Step 2: Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Step 3: Open the spreadsheet (make sure the name matches)
spreadsheet = client.open("Web Scraped Data").sheet1

# Optional: Clear existing content
spreadsheet.clear()

# Step 4: Write titles into the sheet
spreadsheet.update_cell(1, 1, "Headline")
for idx, title in enumerate(titles, start=2):
    spreadsheet.update_cell(idx, 1, title)

print("✅ Headlines successfully written to Google Sheets!")
