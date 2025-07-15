# Automation Scripts

This repository contains automation scripts developed for streamlining repetitive tasks using Python, Selenium, and Google APIs.

## 🚀 Current Projects

### 🗂️ Script 1: Keap CRM Note Appender

This script appends notes from a Google Sheet into Keap CRM contact records.

#### 📄 File:
- `append_keap_notes.py`

#### ✅ What it does:
- Opens each contact record by ID
- Navigates to the Person Notes tab
- Appends new notes from the sheet without overwriting existing data
- Saves the record before moving to the next one

#### 🧪 Example Run:
```bash
python3 append_keap_notes.py
```

#### 📦 Dependencies:
Install with:
```bash
pip3 install -r requirements.txt
```

---

### 🗂️ Script 2: Property Auctions Center Scraper

This script logs into [PropertyAuctionsCenter.com](https://propertyauctionscenter.com) and scrapes data into a Google Sheet.

#### 📄 File:
- `scrape_to_sheet.py`

#### ✅ What it does:
- Logs in using credentials stored in `.env`
- Extracts auction table data
- Appends it to a specified Google Sheet

#### ⚙️ .env format:
```
USERNAME=your_email@example.com
PASSWORD=your_password
LOGIN_URL=https://propertyauctionscenter.com/users/sign_in
GOOGLE_SHEET_NAME=Propertyauctionscenter_table
GOOGLE_CREDENTIALS_FILE=google-credentials.json
```

> 🔒 **Note:** `.env` and `google-credentials.json` are excluded via `.gitignore`.

#### 🧪 Example Run:
```bash
python3 scrape_to_sheet.py
```

#### 📦 Dependencies:
Same as in `requirements.txt`. Install with:
```bash
pip3 install -r requirements.txt
```

