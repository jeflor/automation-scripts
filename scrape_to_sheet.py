from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from gspread.utils import rowcol_to_a1
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")


import time

# ===============================
# 🔐 CONFIGURATION SECTION
# ===============================


# ===============================
# 📊 GOOGLE SHEET CONNECTION
# ===============================
def connect_to_sheet(sheet_name, credentials_file):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

# ===============================
# 🧠 LOGIN + SCRAPE FUNCTION
# ===============================
def login_and_scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    # Step 1: Log in
    driver.get(LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.ID, "user_email"))).send_keys(USERNAME)
    driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    print("🔐 Logged in successfully (headless)")

    # Step 2: Open 'Auction Status' filters
    auction_status_btn = wait.until(EC.element_to_be_clickable((By.ID, "auction-status-dropdown")))
    driver.execute_script("arguments[0].click();", auction_status_btn)
    time.sleep(1)

    # Step 3: Click 'Parcels Data Available' master checkbox
    try:
        checkbox = wait.until(EC.presence_of_element_located((
            By.XPATH, "//label[contains(., 'Parcels Data Available')]/input[@type='checkbox']"
        )))
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)
            print("✅ Checked 'Parcels Data Available'")
        else:
            print("✔️ Already checked")
    except Exception as e:
        print(f"⚠️ Couldn't find checkbox: {e}")

    print("⏳ Waiting for filtered table to load...")
    time.sleep(5)

    # Step 4: Scrape paginated table
    all_data = []
    headers = []
    page_number = 1
    prev_first_row = ""

    while True:
        print(f"📄 Scraping page {page_number}...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        table = driver.find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        if not headers:
            headers = [th.text.strip() for th in rows[0].find_elements(By.TAG_NAME, "th")]
            all_data.append(headers)

        current_first_row = rows[1].text.strip() if len(rows) > 1 else ""
        if current_first_row == prev_first_row:
            print("⚠️ Table didn't change — breaking loop.")
            break
        prev_first_row = current_first_row

        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                processed_row = []
                for i, td in enumerate(cells):
                    text = td.text.strip()
                    if i in [2, 3]:  # Convert date columns (Sale Date and Post Date)
                        try:
                            dt = datetime.strptime(text, "%m/%d/%Y")
                            processed_row.append(dt)  # Pass real datetime
                        except ValueError:
                            processed_row.append(text)
                    else:
                        processed_row.append(text)
                all_data.append(processed_row)

        # Step 5: Click “Next”
        try:
            print("🔎 Looking for 'Next' button...")
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next') and not(contains(@class, 'disabled'))]")))
            driver.execute_script("arguments[0].click();", next_button)
            page_number += 1
            time.sleep(4)
        except Exception as e:
            print(f"✅ Done scraping or no more pages: {e}")
            break

    driver.quit()

    # Step 6: Upload using USER_ENTERED so Google recognizes dates
    try:
        sheet = connect_to_sheet(GOOGLE_SHEET_NAME, GOOGLE_CREDENTIALS_FILE)
        sheet.clear()

        cell_list = []
        for row_idx, row in enumerate(all_data, start=1):
            for col_idx, val in enumerate(row, start=1):
                if isinstance(val, (datetime, date)):
                    cell_list.append(gspread.Cell(row_idx, col_idx, val.strftime("%Y-%m-%d")))
                else:
                    cell_list.append(gspread.Cell(row_idx, col_idx, val))

        sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
        print(f"📤 Uploaded {len(all_data)-1} rows to Google Sheet: {GOOGLE_SHEET_NAME}")
    except Exception as e:
        print(f"❌ Failed to update Google Sheet: {e}")

# ✅ Run the script
if __name__ == "__main__":
    login_and_scrape()
