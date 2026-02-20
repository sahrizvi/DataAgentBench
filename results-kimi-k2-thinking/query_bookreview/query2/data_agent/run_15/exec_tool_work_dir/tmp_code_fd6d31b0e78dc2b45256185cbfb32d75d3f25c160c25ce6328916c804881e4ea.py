code = """import json

print('Loading books data...')

# Load the query results from the file
with open('/tmp/tmpte6o05x9.json', 'r') as f:
    books_sample = json.load(f)

print('Total books in sample:', len(books_sample))

# Check for Literature & Fiction pattern
lit_fiction_books = []
for book in books_sample:
    if 'Literature & Fiction' in book['categories']:
        lit_fiction_books.append(book)

print('Books with Literature & Fiction in sample:', len(lit_fiction_books))

if lit_fiction_books:
    print('First Literature & Fiction book categories:', lit_fiction_books[0]['categories'])

print('Sample categories for first few books:')
for i in range(min(5, len(books_sample))):
    print('Book', i+1, 'categories:', books_sample[i]['categories'][:100])"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json'}

exec(code, env_args)
