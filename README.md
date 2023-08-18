# XML to SQLite Script

This script parses an XML file containing category and teaser data, creates an SQLite database, and populates two tables (`categories` and `teasers`) with the extracted data. It then allows you to query and display the contents of these tables.

## Prerequisites

- Python 3.x
- `xml.etree.ElementTree` module (built-in)
- `re` module (built-in)
- `sqlite3` module (built-in)

## Usage

1. **Install Python**: Make sure you have Python 3.x installed on your system.

2. **Run the Script**: Open a terminal and navigate to the directory containing the script. Run the script using the following command:

python main.py


3. **Database Creation and Data Import**:
- The script reads data from the `data.xml` file and creates an SQLite database named `data.db`.
- Two tables are created in the database: `categories` and `teasers`.
- The script then inserts the extracted data from the XML file into these tables.

4. **Table Display**:
- After importing the data, the script prompts you to enter the name of a table (`teasers` or `categories`) to display its contents.
- To see the results of a table, type its name and press Enter. The data will be displayed in a tabular format.
- To exit the table display mode, type `q` and press Enter.

## Schema

### Categories Table

| Column     | Type  | Description      |
|------------|-------|------------------|
| id         | INTEGER | Primary key     |
| name       | TEXT  | Category name   |

### Teasers Table

| Column     | Type  | Description                     |
|------------|-------|---------------------------------|
| id         | INTEGER | Primary key                    |
| category_id | INTEGER | Foreign key to `categories` table |
| url        | TEXT  | Teaser URL                      |
| picture    | TEXT  | Picture URL                     |
| title      | TEXT  | Teaser title                    |
| vendor     | TEXT  | Vendor name                     |
| text       | TEXT  | Teaser text                     |
| active     | BOOLEAN | Teaser activity status          |

- A foreign key relationship is established between the `teasers` table's `category_id` column and the `categories` table's `id` column, with `ON DELETE CASCADE` behavior. This means that when a category is deleted, the associated teasers will also be deleted.

## Notes

- The script uses batch insertions and transactions to improve performance.
- The script allows you to view the contents of the `categories` and `teasers` tables in a tabular format.

---
