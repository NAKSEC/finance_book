# finance_book
Notebook to manage investment in a specific company. Scraping financial statements to create semi-automated valuation.

## Getting Started

### Prerequisites

```
Virtualenv
Docker
Mongo DB
Scrapy
```

## Installation

Run install.sh or use docker-compose in finance_tools directory

## Modules
* **financestats** - Scraping data from Yahoo Finanace. Used spider lib to scrape the data from yahoo and also use the REST API.
  1. **Maya** - Scraping Israeli companies statements using camelot lib (OCR). Scraping all the tables from the financial statements.
  2. **damodarn** - Scraping data from Damodaran dataset (http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html). Used in WACC calculation.
* **finance_tools** - REST API to all data in the MongoDB. Essential ratio calculations on the financial data for preliminary research.
* **frontend** - Web Portal to create valuations(Vue.js). Use the REST API to get the data. Currently, implement graphs and tables.
