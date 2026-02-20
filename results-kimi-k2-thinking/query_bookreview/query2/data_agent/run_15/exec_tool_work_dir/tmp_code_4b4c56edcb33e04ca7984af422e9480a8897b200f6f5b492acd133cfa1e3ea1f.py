code = """import json
import re

# Load the query results from the file
with open('/tmp/tmpte6o05x9.json', 'r') as f:
    books_sample = json.load(f)

print(f"Total books in sample: {len(books_sample)}")
print("\nFirst few books:")
for i, book in enumerate(books_sample[:5]):
    print(f"\nBook {i+1}:")
    print(f"  ID: {book['book_id']}")
    print(f"  Title: {book['title']}")
    print(f"  Categories: {book['categories']}")
    print(f"  Details: {book['details'][:200]}")

print("\n" + "="*80)
print("Analyzing 'Literature & Fiction' category pattern...")

# Check for Literature & Fiction pattern
lit_fiction_books = []
for book in books_sample:
    if 'Literature & Fiction' in book['categories']:
        lit_fiction_books.append(book)

print(f"Books with 'Literature & Fiction' in sample: {len(lit_fiction_books)}")

if lit_fiction_books:
    print("\nFirst Literature & Fiction book:")
    print(json.dumps(lit_fiction_books[0], indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json'}

exec(code, env_args)
