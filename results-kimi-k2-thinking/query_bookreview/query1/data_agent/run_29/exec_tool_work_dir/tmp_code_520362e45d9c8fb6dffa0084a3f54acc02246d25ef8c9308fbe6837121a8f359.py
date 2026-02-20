code = """import json
import re

# Load the books data
books_path = locals()['var_functions.query_db:5']
with open(books_path, 'r') as f:
    books_data = json.load(f)

# Load the reviews data
reviews_path = locals()['var_functions.query_db:6']
with open(reviews_path, 'r') as f:
    reviews_data = json.load(f)

print("Books loaded:", len(books_data))
print("Reviews loaded:", len(reviews_data))

# Extract publication year from details field
books_with_years = []
for book in books_data:
    details = book.get('details', '')
    # Look for year patterns in details
    year_match = re.search(r'(\d{4})', details)
    if year_match:
        year = int(year_match.group(1))
        book['published_year'] = year
        # Calculate decade
        book['decade'] = f"{year//10*10}s"
        books_with_years.append(book)

print(f"Books with extracted years: {len(books_with_years)}")

# Check sample data
if books_with_years:
    print("Sample book with year:", {
        'title': books_with_years[0]['title'],
        'year': books_with_years[0]['published_year'],
        'decade': books_with_years[0]['decade'],
        'details_snippet': books_with_years[0]['details'][:100]
    })

# Save processed data
with open('/tmp/books_with_decades.json', 'w') as f:
    json.dump(books_with_years, f)

print("__RESULT__:")
print(json.dumps({
    'books_count': len(books_with_years),
    'sample_book': books_with_years[0] if books_with_years else None
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json'}

exec(code, env_args)
