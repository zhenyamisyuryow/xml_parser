import xml.etree.ElementTree as ET
import re
import sqlite3

tree = ET.parse('data.xml')
root = tree.getroot()
namespace = re.match(r'\{.*\}', root.tag).group(0)

#Create db
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

#Defining CREATE queries
categories_create = '''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
'''
teasers_create = '''
    CREATE TABLE IF NOT EXISTS teasers (
        id INTEGER PRIMARY KEY,
        category_id INTEGER,
        url TEXT,
        picture TEXT,
        title TEXT,
        vendor TEXT,
        text TEXT,
        active BOOLEAN,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
'''

#Define table operations (CREATE, INSERT)
def table_operations(create_query: str, insert_params: list):
    cursor.execute(create_query)
    cursor.executemany(insert_params[0], insert_params[1])


def main():
    category_data = []
    teaser_data = []

    #Parsing categories
    for category in root.findall(f'.//{namespace}category'):
        category_id = int(category.get('id'))
        category_name = category.text
        category_data.append((category_id, category_name))

    category_insert = 'INSERT INTO categories (id, name) VALUES (?, ?)'

    #Parsing teasers
    for teaser in root.findall(f'.//{namespace}teaser'):
        teaser_id = int(teaser.get('id'))
        active = "True" if teaser.get('active') == 'true' else "False"
        category_id = int(teaser.find(f'{namespace}categoryId').text)
        url = teaser.find(f'{namespace}url').text
        picture = teaser.find(f'{namespace}picture').text
        title = teaser.find(f'{namespace}title').text
        vendor = teaser.find(f'{namespace}vendor').text
        text = teaser.find(f'{namespace}text').text
        teaser_data.append((teaser_id, category_id, url, picture, title, vendor, text, active))

    teaser_insert = 'INSERT INTO teasers (id, category_id, url, picture, title, vendor, text, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    
    #Run func to CREATE table and INSERT data
    try:
        table_operations(categories_create, [category_insert, category_data])
        table_operations(teasers_create, [teaser_insert, teaser_data])
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category_id ON teasers (category_id)')
        conn.commit()
    except:
        pass


    #Displaying results
    while True:
        user_input = input("Type the name of a table to see the result (Press Q to enter): ").lower()
        if user_input in ["teasers", "categories"]:
            columns = [column[0] for column in cursor.execute(f"SELECT * FROM {user_input}").description]
            rows = cursor.execute(f"SELECT * FROM {user_input}").fetchall()
            print(' | '.join(columns))
            for row in rows:
                print(' | '.join([str(el) for el in row]))
        elif user_input == 'q':
            break
        else:
            print("Invalid table name.")
            continue
    
    conn.close()

if __name__ == "__main__":
    main()