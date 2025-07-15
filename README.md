# Automation Scripts

This repository contains automation scripts developed for streamlining repetitive tasks using Python, Selenium, and Google APIs.

## 🚀 Current Projects

### 1. Keap Note Appender

Automates the process of appending notes to contact records in Keap CRM using data from a connected Google Sheet.

**Features:**
- Opens the contact profile URL from the spreadsheet
- Adds a predefined or dynamic note
- Optionally waits for manual login if session isn't saved
- Clicks "Save" to confirm the note
- Moves on to the next record

---

### 2. Google Sheet Scraper

Automates the process of scraping structured data from a website and updating a Google Sheet.

**Features:**
- Uses Selenium to launch a headless Chrome session
- Navigates to the target website and extracts relevant information
- Authenticates and updates a connected Google Sheet
- Can be triggered manually or scheduled via macOS Automator / `launchd`
- Sends desktop and voice notifications when done
