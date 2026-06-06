# 🎯 Google Maps Lead Finder (Web-Less Lead Generator)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-v1.40%2B-green.svg)](https://playwright.dev/python/)
[![Pandas](https://img.shields.io/badge/pandas-v2.0%2B-orange.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

An automation tool designed to scrape, extract, and filter high-quality business leads directly from Google Maps without requiring any official Google Maps APIs or API keys. It strictly targets **businesses that have a high customer rating but lack a website**, making it the ultimate prospecting tool for web development agencies, SEO freelancers, and digital marketers.

---

## 🚀 Key Features

* **Zero API Keys Required**: Uses Playwright automation in headless mode to fetch actual live Google Maps listings.
* **Smart Filtering Engine**: 
  * ⭐ Filters only businesses with a **Google Rating of 3.5 or higher**.
  * 🌐 Detects and excludes businesses that already have a website.
* **Automated Scrolling**: Simulates realistic human behavior by automatically scrolling through Google Maps listings to load deep search results.
* **Robust Parser**: Parses listings utilizing BeautifulSoup to capture details accurately.
* **CSV Export**: Deduplicates business names and writes the results to a clean UTF-8 CSV file ready for cold email campaigns, cold calling, or CRM importing.

---

## 🛠️ Tech Stack & Requirements

* **Python 3.8+**
* [Playwright (Python Async)](https://playwright.dev/python/) - Headless browser scraping
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Parsing page HTML
* [Pandas](https://pandas.pydata.org/) - Data cleaning, deduplication, and export

---

## 📦 Installation & Setup

Follow these steps to set up the Lead Finder on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/darshgami/BUSSINESS_FINDER.git
cd BUSSINESS_FINDER
```

### 2. Set Up a Virtual Environment (Recommended)
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Web Drivers
Since the tool runs headless Chromium, you must install the Playwright browser binaries:
```bash
playwright install chromium
```

---

## 💻 Usage

Run the `lead_finder.py` script via the command line by supplying the target **city** and the search **query**.

### CLI Arguments:
| Argument | Required | Default | Description |
| :--- | :---: | :---: | :--- |
| `--city` | **Yes** | — | Target city name (e.g., `Rajkot`, `New York`) |
| `--query` | **Yes** | — | Search query/category (e.g., `manufacturers`, `dentists`, `hotels`) |
| `--output` | No | `potential_leads.csv` | Output file name for the generated CSV |

### Examples:

#### 1. Search for manufacturers in Rajkot:
```bash
python lead_finder.py --city "Rajkot" --query "manufacturers" --output "rajkot_manufacturers.csv"
```

#### 2. Search for dentists in New York (using default output file):
```bash
python lead_finder.py --city "New York" --query "dentists"
```

---

## 📊 Output File Structure

The generated CSV will contain the following columns:

| Column Name | Description |
| :--- | :--- |
| `Business Name` | Name of the business/merchant on Google Maps |
| `City` | The target city searched |
| `Google Rating` | Average rating (always $\ge 3.5$) |
| `Address / Contact Info` | Contact address and/or phone numbers if available |

*Note: The script outputs UTF-8-SIG encoding to prevent encoding issues when viewing results directly in Microsoft Excel.*

---

## 🎯 Ideal Prospecting Strategy (For Agencies)

This tool is custom-built to help you source high-converting cold outreach prospects. Here is the recommended workflow:

1. **Find the Leads**: Run the tool to find high-rated businesses without a website.
2. **Qualify**: Check their rating to verify they are a functional business with happy customers, just lacking an online presence.
3. **Outreach Pitch**: Contact them (using address details/contact info, or matching them on social media) with a compelling pitch:
   > *"Hi [Name], I noticed you have a stellar 4.2 rating on Google from local customers, but you don't have a website yet. You could be missing out on up to 50% more local searches! We can build a custom site for you..."*

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create.
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
