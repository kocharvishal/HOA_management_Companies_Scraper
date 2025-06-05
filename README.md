# HOA-USA Management Companies Scraper

This Python script scrapes **Homeowners Association (HOA) management companies** across all 50 U.S. states from [https://hoa-usa.com](https://hoa-usa.com). It collects information about both **Recommended** and **Regular** companies.

## ✅ Features

- Scrapes **Company Name, Website, Phone, Email, Service Area, Description**
- Covers **all 50 U.S. states**
- Differentiates between **Recommended** and **Regular** listings
- Cleans and validates phone numbers, emails, and URLs
- Retries failed requests with backoff
- Outputs a clean `.csv` file with timestamp
- Logs progress and errors

## 🛠 Requirements

- Python 3.7+
- Install required packages:

```bash
pip install requests pandas beautifulsoup4
```

## 🚀 How to Run

### 🔁 Option 1: Scrape All 50 States

```bash
python hoa_scraper.py --all
```

### 🔁 Option 2: Scrape Specific States

```bash
python hoa_scraper.py --states California Texas Florida
```

### 🕓 Optional: Add Custom Delay Between Requests (default is 2 seconds)

```bash
python hoa_scraper.py --all --delay 5
```

## 🗂 Output

- The output will be saved in the current directory as:

```
hoa_companies_YYYYMMDD_HHMMSS.csv
```

- Columns:
  - `name`
  - `state`
  - `section_type` (`recommended` or `regular`)
  - `phone`
  - `email`
  - `website`
  - `service_area`
  - `description`

## 📌 Notes

- **Recommended companies** have rich data and are handled using structured HTML tags.
- **Regular companies** have limited structure, parsed using pattern matching.
- If no state is specified, the script defaults to scraping **Alabama** (for testing).

## 📋 Example Logs

```
2025-06-05 18:32:12 - INFO - Fetching: https://hoa-usa.com/management-directory/?state=Texas
2025-06-05 18:32:15 - INFO - Found 42 companies for Texas (Recommended: 8, Regular: 34)
```

## 🧼 Cleaning Details

- Phone numbers are normalized to `(XXX) XXX-XXXX` format.
- Email and websites are stripped and validated using regex.
- Duplicate companies (by name + state) are removed.
