# Automation Scripts

This repository contains automation scripts developed for streamlining repetitive tasks using Python, Selenium, and Google APIs.

## 🚀 Current Projects

### 1. Keap Note Appender

Automates the process of appending notes to contact records in Keap CRM using data from a connected Google Sheet.

#### Features
- Opens the contact profile URL from the spreadsheet
- Adds a predefined or dynamic note
- Optionally waits for manual login if session isn't saved
- Clicks "Save" to confirm the note
- Moves on to the next record

#### Requirements
- Python 3.9+
- Selenium
- ChromeDriver
- `google-credentials.json` (not included for security reasons)

#### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/jeflor/automation-scripts.git
    cd automation-scripts
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Place your `google-credentials.json` file in the root (ignored by `.gitignore`).

5. Run the script:
    ```bash
    python append_keap_notes.py
    ```

## 🔐 Security Notice

Do not commit sensitive files like `google-credentials.json`. This repo includes `.gitignore` rules to prevent such files from being pushed.

## 🧭 Roadmap

- [ ] Add logging for success/failure notes
- [ ] Integrate headless browser mode
- [ ] Add support for multiple CRMs
- [ ] Create a GUI wrapper for non-technical users

---

Contributions welcome! Submit an issue or pull request if you have improvements or questions.
# automation-scripts
