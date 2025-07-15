import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

print("🚀 Script started")

# --- GOOGLE SHEETS SETUP ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Import_Paul_notes").sheet1
data = sheet.get_all_values()[1:]  # Skip header

if not data:
    print("❌ No data found in sheet.")
    exit()

# --- SELENIUM SETUP ---
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# --- PAUSE TO LOG INTO KEAP FIRST ---
driver.get("https://m293.infusionsoft.com/Login")
input("⏸️ Log into Keap in the browser, then press Enter here to begin processing...")

# --- PROCESS EACH CONTACT ---
for row in data:
    contact_id = row[0].strip()
    new_note = row[1].strip()

    if not contact_id or not new_note:
        print(f"⚠️ Skipping blank row")
        continue

    print(f"\n🔗 Opening contact ID {contact_id}")
    url = f"https://m293.infusionsoft.com/Contact/oldManageContact_legacy.jsp?view=edit&ID={contact_id}"
    driver.get(url)

    # Wait for page to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "Contact0FirstName"))
        )
        print("✅ Contact page loaded.")
    except TimeoutException:
        print(f"❌ Failed to load page for ID {contact_id}")
        continue

    # Click 'Person Notes' tab
    try:
        notes_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Person Notes"))
        )
        notes_tab.click()
        print("✅ Clicked 'Person Notes' tab.")
    except Exception as e:
        print(f"❌ Failed to click Notes tab: {e}")
        continue

    # Locate and update notes
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Contact0ContactNotes"))
        )
        textarea = driver.find_element(By.ID, "Contact0ContactNotes")
        existing_note = textarea.get_attribute("value")
    except Exception as e:
        print(f"❌ Could not find notes field: {e}")
        continue

    # Append new note
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    updated_note = f"{existing_note}\n\n--- {timestamp} ---\n{new_note}"

    textarea.clear()
    textarea.send_keys(updated_note)
    print("✏️ Note appended.")

    # Click Save
    try:
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Save"))
        )
        save_button.click()
        print(f"✅ Clicked Save for ID {contact_id}")
        time.sleep(4)  # allow save to complete
    except Exception as e:
        print(f"❌ Save failed for ID {contact_id}: {e}")
        input("🛑 Fix manually, then press Enter to continue to next contact...")

# --- DONE ---
print("\n🎉 All contacts processed.")
driver.quit()
