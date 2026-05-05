import sqlite3
import os

DB_PATH = 'database.sqlite'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dealerships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        name TEXT NOT NULL,
        panel_path TEXT NOT NULL,
        logo_dark_path TEXT,
        logo_light_path TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts (id)
    )
    ''')

    # Seed Brands
    brands = ['Tata', 'Volkswagen']
    for brand in brands:
        cursor.execute('INSERT OR IGNORE INTO accounts (name) VALUES (?)', (brand,))

    # Get brand IDs
    cursor.execute('SELECT id, name FROM accounts')
    brand_map = {name: id for id, name in cursor.fetchall()}

    # Seed Dealerships from assets
    assets_base = 'assets/Dealership-panels'
    
    # Tata Dealers
    tata_path = os.path.join(assets_base, 'Tata-dealers')
    if os.path.exists(tata_path):
        for dealer_dir in os.listdir(tata_path):
            full_path = os.path.join(tata_path, dealer_dir)
            if os.path.isdir(full_path):
                cursor.execute('''
                    INSERT INTO dealerships (account_id, name, panel_path, logo_dark_path, logo_light_path)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    brand_map['Tata'], 
                    dealer_dir, 
                    os.path.join(full_path, 'template.png'),
                    os.path.join(full_path, 'logo-dark.png'),
                    os.path.join(full_path, 'logo-light.png')
                ))

    # VW Dealers
    vw_path = os.path.join(assets_base, 'VW-dealers')
    if os.path.exists(vw_path):
        for dealer_dir in os.listdir(vw_path):
            full_path = os.path.join(vw_path, dealer_dir)
            if os.path.isdir(full_path):
                cursor.execute('''
                    INSERT INTO dealerships (account_id, name, panel_path, logo_dark_path, logo_light_path)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    brand_map['Volkswagen'], 
                    dealer_dir, 
                    os.path.join(full_path, 'template.png'),
                    os.path.join(full_path, 'logo-dark.png'),
                    os.path.join(full_path, 'logo-light.png')
                ))

    conn.commit()
    conn.close()
    print("Database initialized and seeded successfully.")

if __name__ == '__main__':
    init_db()
