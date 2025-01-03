import sqlite3

connection = sqlite3.connect('products.db')
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
    cursor.execute('DELETE FROM Products')

    for i in range(1,5):
        cursor.execute(
            'INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
            (f'Продукт {i}', f'Описание {i}', i * 100)
        )
    connection.commit()



def get_all_products():
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()

if __name__ == '__main__':
    initiate_db()
    connection.close()
