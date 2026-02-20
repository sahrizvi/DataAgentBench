code = """import json

# Get the file paths using the dictionary properly
vars_dict = globals()
children_books_file_path = '/tmp/tmp0e5vhf4x.json'
reviews_2020_file_path = '/tmp/tmpxf5c0b0y.json'

# Read children's books data
with open(children_books_file_path, 'r') as f:
    children_books = json.load(f)

# Read reviews from 2020 onwards
with open(reviews_2020_file_path, 'r') as f:
    reviews_2020 = json.load(f)

# Extract book IDs from children's books
children_book_ids = set()
for book in children_books:
    # Extract the numeric ID from book_id (e.g., "bookid_4" -> "4")
    try:
        book_num = book['book_id'].split('_')[1]
        children_book_ids.add(book_num)
    except:
        pass

# Filter reviews for children's books and calculate averages
from collections import defaultdict

children_reviews = defaultdict(list)
for review in reviews_2020:
    purchase_id = review['purchase_id']
    # Extract the numeric ID from purchase_id (e.g., "purchaseid_4" -> "4")
    try:
        purchase_num = purchase_id.split('_')[1]
        if purchase_num in children_book_ids:
            children_reviews[purchase_num].append(float(review['rating']))
    except:
        pass

# Calculate average ratings
qualified_books = []
for book_num, ratings in children_reviews.items():
    avg_rating = sum(ratings) / len(ratings)
    if avg_rating >= 4.5:
        # Find the corresponding book info
        for book in children_books:
            if book_num in book['book_id']:
                qualified_books.append({
                    'title': book['title'],
                    'book_id': book['book_id'],
                    'average_rating': avg_rating,
                    'review_count': len(ratings)
                })
                break

result = {
    'qualified_books': qualified_books,
    'total_count': len(qualified_books)
}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json'}

exec(code, env_args)
