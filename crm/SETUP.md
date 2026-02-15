# Google Sheets CRM Setup Guide

## Prerequisites
- Google account
- Python 3.8+
- `gspread` and `google-auth` packages installed (`pip install -r requirements.txt`)

## Step-by-Step Setup

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** (top bar) → **New Project**
3. Name it `Goldmans LeadGen` → **Create**
4. Make sure the new project is selected in the top bar

### 2. Enable APIs
1. Go to **APIs & Services** → **Library**
2. Search for **Google Sheets API** → Click it → **Enable**
3. Search for **Google Drive API** → Click it → **Enable**

### 3. Create Service Account
1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **Service account**
3. Name: `goldmans-crm` → **Create and Continue**
4. Role: skip (no role needed) → **Continue** → **Done**
5. Click on the new service account email in the list
6. Go to **Keys** tab → **Add Key** → **Create new key**
7. Choose **JSON** → **Create**
8. Save the downloaded file as `credentials.json` in the project root

### 4. Create the Google Sheet
1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new blank spreadsheet
3. Rename it to `Goldman's CRM`
4. Copy the **spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```

### 5. Share Sheet with Service Account
1. Open `credentials.json` and find the `client_email` field
   (looks like `goldmans-crm@goldmans-leadgen.iam.gserviceaccount.com`)
2. In Google Sheets, click **Share**
3. Paste the service account email → Set to **Editor** → **Send**

### 6. Configure Environment Variables
Add to your `.env` file:
```
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=your_spreadsheet_id_here
```

### 7. Initialize CRM Tabs
Run the initialization command to create all 5 tabs with headers and formulas:
```bash
python crm/sheets_manager.py --init
```

This is safe to re-run — it only creates tabs that don't already exist.

## Verify Setup
```bash
# Check connection and view dashboard
python crm/sheets_manager.py --dashboard

# Test with dry-run mode (no API calls)
python crm/sheets_manager.py --dry-run --dashboard
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `FileNotFoundError: credentials.json` | Check `GOOGLE_SHEETS_CREDENTIALS` path in `.env` |
| `gspread.exceptions.SpreadsheetNotFound` | Verify `GOOGLE_SHEETS_ID` in `.env` is correct |
| `gspread.exceptions.APIError 403` | Share the sheet with the service account email |
| `google.auth.exceptions.DefaultCredentialsError` | Re-download the JSON key from Google Cloud Console |

## Sheet Structure

The CRM uses 5 tabs:
1. **Leads** — Master lead database with status tracking
2. **Outreach Log** — Every email, SMS, and call touchpoint
3. **Referral Partners** — Partner relationship tracking
4. **Campaigns** — Campaign performance metrics
5. **Dashboard** — Auto-calculated summary metrics
