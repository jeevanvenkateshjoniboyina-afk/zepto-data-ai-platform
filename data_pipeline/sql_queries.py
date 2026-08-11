"""
==========================================================
Project : Zepto Data & AI Platform
Module  : Module 1 - Data Pipeline

File    : sql_queries.py

Author  : Joniboyina Jeevan Venkatesh

Description:
Execute SQL queries on the books database.
==========================================================
"""

import sqlite3
import pandas as pd

DATABASE_FILE = "data_pipeline/books.db"


def create_connection():
    """Create database connection."""

    connection = sqlite3.connect(DATABASE_FILE)

    return connection
def query_1(connection):
    """
    Books having rating greater than or equal to 4.
    """

    print("\nQUERY 1 : SELECT + WHERE\n")

    query = """
    SELECT title, rating
    FROM books
    WHERE rating >= 4;
    """

    df = pd.read_sql(query, connection)

    print(df)

    return df
def query_2(connection):
    """
    Top 10 expensive books.
    """

    print("\nQUERY 2 : ORDER BY + LIMIT\n")

    query = """
    SELECT title, price_inr
    FROM books
    ORDER BY price_inr DESC
    LIMIT 10;
    """

    df = pd.read_sql(query, connection)

    print(df)

    return df
def query_3(connection):
    """
    Display all unique book categories.
    """

    print("\n" + "="*60)
    print("QUERY 3 : DISTINCT")
    print("="*60)

    query = """
    SELECT DISTINCT category_name
    FROM categories;
    """

    df = pd.read_sql(query, connection)

    print(df)

    return df
def query_4(connection):
    """
    Books whose rating is between 3 and 5.
    """

    print("\n" + "="*60)
    print("QUERY 4 : BETWEEN")
    print("="*60)

    query = """
    SELECT title, rating
    FROM books
    WHERE rating BETWEEN 3 AND 5;
    """

    df = pd.read_sql(query, connection)

    print(df)

    return df
def query_5(connection):
    """
    Books having rating 4 or 5.
    """

    print("\n" + "="*60)
    print("QUERY 5 : IN")
    print("="*60)

    query = """
    SELECT title, rating
    FROM books
    WHERE rating IN (4, 5);
    """

    df = pd.read_sql(query, connection)

    print(df)

    return df
def query_6(connection):
    """
    Join books and categories tables.
    """

    print("\n" + "="*60)
    print("QUERY 6 : JOIN")
    print("="*60)

    query = """
    SELECT
        books.title,
        books.price_inr,
        books.rating,
        categories.category_name
    FROM books
    INNER JOIN categories
    ON books.category_id = categories.category_id;
    """

    df = pd.read_sql(query, connection)

    print(df)

    return df

def main():

    connection = create_connection()

    query_1(connection)
    query_2(connection)
    query_3(connection)
    query_4(connection)
    query_5(connection)
    query_6(connection)

    connection.close()

    print("\nAll SQL queries executed successfully.")


if __name__ == "__main__":
    main()