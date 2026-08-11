"""
==========================================================
Project : Zepto Data & AI Platform
Module  : Module 1 - Data Pipeline

File    : scrape_books.py

Author  : Joniboyina Jeevan Venkatesh

Description:
------------
This script scrapes book data from the public website
https://books.toscrape.com.

It performs the following tasks:
1. Scrapes book information from the first 5 catalogue pages.
2. Cleans the extracted data.
3. Converts GBP prices into INR using:
       1 GBP = 105.50 INR
4. Saves the cleaned dataset as books.csv.

Course:
IIT Patna AIML Capstone Project
==========================================================
"""
import requests
import pandas as pd

from bs4 import BeautifulSoup
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

TOTAL_PAGES = 5

GBP_TO_INR = 105.50

OUTPUT_FILE = "data_pipeline/books.csv"
def fetch_page(url):
    """
    Downloads a webpage and returns a BeautifulSoup object.

    Parameters:
        url (str): URL of the webpage.

    Returns:
        BeautifulSoup: Parsed HTML if successful.
        None: If the request fails.
    """

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")

        print(f"Failed to fetch page: {url}")
        print(f"Status Code: {response.status_code}")

        return None

    except Exception as e:
        print(f"Error while fetching page: {e}")
        return None


def parse_book(book):
    """
    Extract book information from one book card.

    Parameters:
        book (Tag): BeautifulSoup article tag containing one book.

    Returns:
        dict: Dictionary containing book details.
    """

    title = book.h3.a["title"]

    price = book.find("p", class_="price_color").text.strip()

    rating = book.find("p")["class"][1]

    availability = book.find(
        "p",
        class_="instock availability"
    ).text.strip()

    category = "All Books"

    return {
        "title": title,
        "price": price,
        "star_rating": rating,
        "availability": availability,
        "category": category
    }


def scrape_books():
    """
    Scrape all books from the first five catalogue pages.

    Returns:
        list: List of dictionaries containing book details.
    """

    all_books = []

    for page in range(1, TOTAL_PAGES + 1):

        print(f"\nLoading Page {page}...")

        url = BASE_URL.format(page)

        soup = fetch_page(url)

        if soup is None:
            continue

        books = soup.find_all("article", class_="product_pod")

        print(f"Found {len(books)} books")

        for book in books:

            book_data = parse_book(book)

            all_books.append(book_data)

    print(f"\nTotal Books Scraped : {len(all_books)}")

    return all_books


def clean_data(df):
    """
    Clean the scraped book data.

    - Convert price to float
    - Convert star rating to integer
    - Convert availability to boolean
    - Handle parsing errors
    """

    # Convert price (£51.77 -> 51.77)
    df["price_gbp"] = (
    df["price"]
    .str.replace("Â", "", regex=False)
    .str.replace("£", "", regex=False)
    .str.strip()
    )

# Convert safely to numeric
    df["price_gbp"] = pd.to_numeric(
        df["price_gbp"],
        errors="coerce"
    )

    # Convert star rating text to integer
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["star_rating"].map(rating_map)

    # Convert availability to boolean
    df["in_stock"] = df["availability"].str.contains(
        "In stock",
        case=False,
        na=False
    )

    # Handle numeric parsing failures
    if df["price_gbp"].isnull().any():
        median_price = df["price_gbp"].median()
        df["price_gbp"] = df["price_gbp"].fillna(median_price)

    if df["rating"].isnull().any():
        median_rating = int(df["rating"].median())
        df["rating"] = df["rating"].fillna(median_rating)

    return df


def convert_currency(df):
    """
    Convert book prices from GBP to INR.
    """

    df["price_inr"] = (
        df["price_gbp"] * GBP_TO_INR
    ).round(2)

    return df


def save_csv(df):
    """
    Save cleaned dataset to CSV.
    """

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nDataset saved as {OUTPUT_FILE}")


def main():

    print("=" * 60)
    print("MODULE 1 : DATA PIPELINE")
    print("=" * 60)

    books = scrape_books()

    df = pd.DataFrame(books)

    print("\nCleaning data...")
    df = clean_data(df)

    print("Converting GBP to INR...")
    df = convert_currency(df)

    print("Saving dataset...")
    save_csv(df)

    print("\nDataset Preview:\n")
    print(df.head())

    print("\nDataset Information\n")
    print(df.info())

    print("\nShape :", df.shape)

    print("\nPipeline completed successfully.")
if __name__ == "__main__":
    main()