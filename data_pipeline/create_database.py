"""
==========================================================

Project : Zepto Data & AI Platform

Module : Module 1 – Data Pipeline

File : create_database.py

Author : Joniboyina Jeevan Venkatesh

Description

Creates a normalized SQLite database from the
cleaned books.csv dataset.

Creates

1. Categories Table

2. Books Table

3. Primary Key

4. Foreign Key

==========================================================
"""
import sqlite3
import pandas as pd
CSV_FILE = "data_pipeline/books.csv"
DATABASE_FILE = "data_pipeline/books.db"
def create_connection():
    """
    Create SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    print("Database Connected Successfully.")

    return connection
def create_tables(connection):
    """
    Create the required database tables.
    """

    cursor = connection.cursor()

    # Create Categories Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE
        )
    """)

    # Create Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price_gbp REAL,
            price_inr REAL,
            rating INTEGER,
            in_stock INTEGER,
            category_id INTEGER,
            FOREIGN KEY(category_id)
                REFERENCES categories(category_id)
        )
    """)

    connection.commit()

    print("Tables Created Successfully.")
def load_dataset():
    """
    Load the cleaned dataset from CSV.

    Returns:
        pandas.DataFrame: Book dataset.
    """

    df = pd.read_csv(CSV_FILE)

    print(f"Dataset Loaded Successfully. Total Books: {len(df)}")

    return df
def insert_categories(connection, df):
    """
    Insert unique categories into the categories table.
    """

    cursor = connection.cursor()

    categories = df["category"].unique()

    for category in categories:
        cursor.execute(
            """
            INSERT OR IGNORE INTO categories(category_name)
            VALUES (?)
            """,
            (category,)
        )

    connection.commit()

    print(f"Inserted {len(categories)} categories.")
def insert_books(connection, df):
    """
    Insert books into the books table.
    """

    cursor = connection.cursor()

    for _, row in df.iterrows():

        # Get category_id
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (row["category"],)
        )

        category_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO books
            (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                row["rating"],
                int(row["in_stock"]),   # True -> 1, False -> 0
                category_id
            )
        )

    connection.commit()

    print(f"Inserted {len(df)} books.")
def main():

    connection = create_connection()

    create_tables(connection)

    df = load_dataset()

    insert_categories(connection, df)

    insert_books(connection, df)

    connection.close()

    print("\nDatabase Created Successfully.")
if __name__ == "__main__":
    main()