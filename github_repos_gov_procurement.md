I'll search for repositories that focus on scraping or sourcing government decision makers and procurement data.Based on my search, there are several relevant GitHub repositories and resources for scraping government procurement and decision-maker data across multiple levels of government. Here's what I found:

## Key Repositories for Government Procurement Scraping

### 1. **Open RFPs Scrapers** (Most Relevant)
- **Repository:** [dobtco/openrfps-scrapers](https://github.com/dobtco/openrfps-scrapers)
- **Purpose:** Specifically designed to scrape and standardize government contracting opportunities, RFPs, and awards across US states and cities
- **Language:** Node.js/JavaScript
- **Why it's useful:** Each government agency has its own directory with specific scrapers. You could extend this to focus on food and grocery supplier contracts by configuring target URLs and filters

### 2. **Procurement Data Topic on GitHub**
- **Link:** [github.com/topics/procurement-data](https://github.com/topics/procurement-data)
- **Notable projects in this topic:**
  - `makegov/procurement-tools` - Python tools for analyzing federal procurement contracts
  - `sumeetkd/govtenders` - Bot to scrape e-procurement websites (adaptable to specific sectors)
  - `crahal/NHSSpend` - Spend data scrapers
  - `kabante/phlcovidcontracts` - Open contracts dataset (code reusable for other jurisdictions)

### 3. **Lead Generation & Decision-Maker Scrapers**
From my search, I also found some advanced lead generation repositories that could help identify government decision-makers:
- **Haskz13/leadgen** - Contains AI-powered scrapers for finding organizational opportunities with decision-maker identification
- **shwetaskumar/sales_lead_scraper** - Advanced lead scraping with entity classification for identifying decision-makers

## How to Adapt These for Your Use Case

1. **Start with Open RFPs Scrapers** and configure it to:
   - Target food/grocery/restaurant procurement contracts
   - Filter by NAICS codes related to food supply
   - Extract decision-maker information from RFP documents

2. **Combine with web scraping frameworks** like:
   - [Scrapy](https://github.com/scrapy/scrapy) (Python)
   - [Puppeteer](https://github.com/puppeteer/puppeteer) (JavaScript/Node.js)

3. **Data sources to target:**
   - SAM.gov (federal contracts)
   - State purchasing agencies' procurement portals
   - City/municipal procurement websites
   - Local government contract databases

---

**Note:** The search results are limited and there may be additional specialized repositories available. For a more comprehensive search, I recommend visiting [github.com/topics/procurement-data](https://github.com/topics/procurement-data) to explore all projects tagged with procurement data.