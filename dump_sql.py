import sqlite3

def dump_sql():
    conn = sqlite3.connect('database.sqlite')
    with open('database.sql', 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    conn.close()
    print("SQL dump generated successfully.")

if __name__ == '__main__':
    dump_sql()
