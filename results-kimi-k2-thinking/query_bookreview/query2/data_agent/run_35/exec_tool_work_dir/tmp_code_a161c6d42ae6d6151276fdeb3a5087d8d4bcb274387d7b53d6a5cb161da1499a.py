code = """import json

# Access the books data from storage
data = locals()['var_functions.query_db:2']

print('__RESULT__:')
result_data = {
    'sample_books': [],
    'fiction_count': 0
}

# Check categories structure
for i, book in enumerate(data[:5]):
    sample_book = {
        'title': book['title'],
        'categories': str(book['categories']),
        'categories_type': str(type(book['categories']))
    }
    result_data['sample_books'].append(sample_book)

# Look for Literature & Fiction in categories
fiction_books = []
for book in data:
    if book['categories'] and 'Literature & Fiction' in str(book['categories']):
        fiction_books.append(book['title'])

result_data['fiction_count'] = len(fiction_books)
result_data['sample_fiction'] = fiction_books[:5]

# Check details field for language info
result_data['details_samples'] = []
for i, book in enumerate(data[:5]):
    if book['details']:
        detail_sample = {
            'title': book['title'],
            'details_snippet': str(book['details'])[:200]
        }
        result_data['details_samples'].append(detail_sample)

print(json.dumps(result_data))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review']}

exec(code, env_args)
