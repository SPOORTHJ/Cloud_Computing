import json
import os
import sqlite3
from typing import List


def connect(path: str) -> sqlite3.Connection:
    """
    Connect to the SQLite database. Creates tables if they don't exist.

    Args:
        path (str): Path to the SQLite database.

    Returns:
        sqlite3.Connection: Connection object to the database.
    """
    db_exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    if not db_exists:
        create_tables(conn)
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create the required tables in the database.

    Args:
        conn (sqlite3.Connection): Connection object to the database.
    """
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()


def get_cart(username: str) -> List[dict]:
    """
    Retrieve the cart for a specific username.

    Args:
        username (str): The username to retrieve the cart for.

    Returns:
        List[dict]: A list of items in the cart.
    """
    conn = connect('carts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM carts WHERE username = ?', (username,))
    cart_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(row) for row in cart_rows] if cart_rows else []


def add_to_cart(username: str, product_id: int) -> None:
    """
    Add a product to the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The product ID to add to the cart.
    """
    conn = connect('carts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    result = cursor.fetchone()
    contents = json.loads(result['contents']) if result and result['contents'] else []
    contents.append(product_id)

    cursor.execute(
        '''
        INSERT INTO carts (username, contents, cost)
        VALUES (?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET contents = excluded.contents
        ''',
        (username, json.dumps(contents), 0)
    )
    conn.commit()
    cursor.close()
    conn.close()


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Remove a product from the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The product ID to remove from the cart.
    """
    conn = connect('carts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    result = cursor.fetchone()
    if not result or not result['contents']:
        cursor.close()
        conn.close()
        return

    contents = json.loads(result['contents'])
    if product_id in contents:
        contents.remove(product_id)

        cursor.execute(
            '''
            UPDATE carts
            SET contents = ?
            WHERE username = ?
            ''',
            (json.dumps(contents), username)
        )
        conn.commit()

    cursor.close()
    conn.close()


def delete_cart(username: str) -> None:
    """
    Delete the cart for a specific username.

    Args:
        username (str): The username to delete the cart for.
    """
    conn = connect('carts.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()

    cursor.close()
    conn.close()
