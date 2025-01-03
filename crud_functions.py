import sqlite3

connection = sqlite3.connect('products2.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')
    cursor.execute('DELETE FROM products')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance INTEGER NOT NULL
            )
        ''')
    cursor.execute('DELETE FROM products')

    for i in range(1,5):
        cursor.execute(
            'INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
            (f'Продукт {i}', f'Описание {i}', i * 100)
        )
    connection.commit()


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()

def add_user(username, email, age):
    cursor.execute(
        'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
        (username, email, age, 1000)
    )
    connection.commit()

def is_included(username):
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    return cursor.fetchone() is not None


if __name__ == '__main__':
    initiate_db()
    connection.close()
