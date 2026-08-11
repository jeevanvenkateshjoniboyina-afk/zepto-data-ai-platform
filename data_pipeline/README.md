# Module 1 – Data Pipeline

## Overview

This module implements a complete data engineering pipeline for scraping book data from BooksToScrape, cleaning the dataset, converting prices from GBP to INR, storing the cleaned data in a normalized SQLite database, and querying the database using SQL and pandas.

---

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite

---

## Dataset

Source:

https://books.toscrape.com/

Books scraped:

- First 5 catalogue pages
- 100 books

---

## Data Cleaning

The following cleaning operations were performed:

- Removed currency symbol from prices.
- Converted prices to float.
- Converted star ratings into integers.
- Converted availability into Boolean values.
- Handled parsing failures using median imputation for numeric fields.

---

## Currency Conversion

Fixed conversion rate used:

**1 GBP = 105.50 INR**

---

## Database Schema

Two normalized tables:

### Categories

- category_id
- category_name

### Books

- book_id
- title
- price_gbp
- price_inr
- rating
- in_stock
- category_id

---

## SQL Operations

Implemented:

- SELECT
- WHERE
- ORDER BY
- LIMIT
- DISTINCT
- BETWEEN
- IN
- INNER JOIN

---

## Pandas Operations

- pd.read_sql()
- pd.merge()

---

## Run Instructions

Run the files in the following order:

```bash
python data_pipeline/scrape_books.py

python data_pipeline/create_database.py

python data_pipeline/sql_queries.py
```
