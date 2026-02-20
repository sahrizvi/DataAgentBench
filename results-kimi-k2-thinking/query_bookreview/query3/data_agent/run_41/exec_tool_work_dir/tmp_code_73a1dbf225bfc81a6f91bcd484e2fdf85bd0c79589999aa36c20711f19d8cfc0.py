code = """import json
from collections import defaultdict

# Load children's books
books_file = 'file_storage/functions.query_db:62.json'
with open(books_file, 'r') as f:
    children_books = json.load(f)

# Load 2020+ reviews  
reviews_file = 'file_storage/functions.query_db:63.json'
with open(reviews_file, 'r') as f:
    reviews_2020 = json.load(f)

# Map book_id to book info
book_dict = {book['book_id']: book for book in children_books}

# Calculate average ratings for children's books with 2020+ reviews
book_ratings = defaultdict(list)
for review in reviews_2020:
    purchase_id = review['purchase_id']
    book_id = purchase_id.replace('purchaseid_', 'bookid_')
    if book_id in book_dict:
        rating = float(review['rating'])
        book_ratings[book_id].append(rating)

# Find qualifying books
results = []
for book_id, ratings in book_ratings.items():
    avg_rating = sum(ratings) / len(ratings)
    if avg_rating >= 4.5:
        book = book_dict[book_id]
        author = book['author']
        if isinstance(author, str) and author.startswith('{'):
            try:
                author_data = json.loads(author.replace("'", '"'))
                if isinstance(author_data, dict) and 'name' in author_data:
                    author = author_data['name']
            except:
                author = 'Unknown'
        elif author is None or author == 'None':
            author = 'Unknown'
        results.append({
            'title': book['title'],
            'author': author,
            'average_rating': round(avg_rating, 2),
            'review_count': len(ratings)
        })

results.sort(key=lambda x: (-x['average_rating'], -x['review_count']))

lines = []
if not results:
    lines.append('No children books found with average rating >= 4.5 based on 2020+ reviews')
else:
    lines.append('Children Books with Average Rating >= 4.5 (2020 onwards):')
    lines.append('')
    for i, book in enumerate(results, 1):
        lines.append(f'{i}. {book["title"]}')
        lines.append(f'   Author: {book["author"]}')
        lines.append(f'   Rating: {book["average_rating"]} ({book["review_count"]} reviews)')
        lines.append('')
        
output = '\n'.join(lines)

print('__RESULT__:')
print(json.dumps(output))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': [], 'var_functions.execute_python:12': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.list_db:5', 'var_functions.query_db:7'], 'var_functions.query_db:14': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.execute_python:30': ['var_functions.query_db:2', 'var_functions.query_db:7', 'var_functions.query_db:14', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28'], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json', 'var_functions.query_db:33': 'file_storage/functions.query_db:33.json', 'var_functions.execute_python:36': {'books_key': 'var_functions.query_db:32', 'reviews_key': 'var_functions.query_db:33', 'all_keys': [{'var_functions.query_db:2': 'file_storage/functions.query_db:2.json'}, {'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}, {'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}, {'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}, {'var_functions.query_db:26': 'file_storage/functions.query_db:26.json'}]}, 'var_functions.execute_python:38': ['var_functions.query_db:2', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28', 'var_functions.query_db:32', 'var_functions.query_db:33'], 'var_functions.execute_python:40': {'books_count': 25, 'reviews_count': 329, 'sample_book': {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'author': 'None'}, 'sample_review': {'rating': '5', 'purchase_id': 'purchaseid_8'}}, 'var_functions.execute_python:42': 'file_storage/functions.execute_python:42.json', 'var_functions.execute_python:46': 'file_storage/functions.execute_python:46.json', 'var_functions.query_db:50': 'file_storage/functions.query_db:50.json', 'var_functions.query_db:51': 'file_storage/functions.query_db:51.json', 'var_functions.query_db:54': 'file_storage/functions.query_db:54.json', 'var_functions.query_db:55': 'file_storage/functions.query_db:55.json', 'var_functions.query_db:58': 'file_storage/functions.query_db:58.json', 'var_functions.query_db:59': 'file_storage/functions.query_db:59.json', 'var_functions.query_db:62': 'file_storage/functions.query_db:62.json', 'var_functions.query_db:63': [{'rating': '5', 'purchase_id': 'purchaseid_8'}, {'rating': '5', 'purchase_id': 'purchaseid_76'}, {'rating': '2', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'purchase_id': 'purchaseid_23'}, {'rating': '2', 'purchase_id': 'purchaseid_99'}, {'rating': '4', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'purchase_id': 'purchaseid_20'}, {'rating': '5', 'purchase_id': 'purchaseid_83'}, {'rating': '3', 'purchase_id': 'purchaseid_67'}, {'rating': '5', 'purchase_id': 'purchaseid_62'}, {'rating': '5', 'purchase_id': 'purchaseid_38'}, {'rating': '5', 'purchase_id': 'purchaseid_4'}, {'rating': '3', 'purchase_id': 'purchaseid_158'}, {'rating': '5', 'purchase_id': 'purchaseid_6'}, {'rating': '4', 'purchase_id': 'purchaseid_158'}, {'rating': '5', 'purchase_id': 'purchaseid_115'}, {'rating': '5', 'purchase_id': 'purchaseid_46'}, {'rating': '5', 'purchase_id': 'purchaseid_83'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_33'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_62'}, {'rating': '5', 'purchase_id': 'purchaseid_62'}, {'rating': '4', 'purchase_id': 'purchaseid_32'}, {'rating': '4', 'purchase_id': 'purchaseid_193'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_13'}, {'rating': '5', 'purchase_id': 'purchaseid_76'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_130'}, {'rating': '5', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'purchase_id': 'purchaseid_8'}, {'rating': '2', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'purchase_id': 'purchaseid_161'}, {'rating': '5', 'purchase_id': 'purchaseid_41'}, {'rating': '5', 'purchase_id': 'purchaseid_145'}, {'rating': '4', 'purchase_id': 'purchaseid_20'}, {'rating': '5', 'purchase_id': 'purchaseid_32'}, {'rating': '5', 'purchase_id': 'purchaseid_196'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_5'}, {'rating': '5', 'purchase_id': 'purchaseid_83'}, {'rating': '2', 'purchase_id': 'purchaseid_5'}, {'rating': '5', 'purchase_id': 'purchaseid_12'}, {'rating': '5', 'purchase_id': 'purchaseid_8'}, {'rating': '5', 'purchase_id': 'purchaseid_140'}, {'rating': '4', 'purchase_id': 'purchaseid_8'}, {'rating': '5', 'purchase_id': 'purchaseid_85'}, {'rating': '5', 'purchase_id': 'purchaseid_94'}, {'rating': '4', 'purchase_id': 'purchaseid_72'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '4', 'purchase_id': 'purchaseid_8'}, {'rating': '5', 'purchase_id': 'purchaseid_20'}, {'rating': '5', 'purchase_id': 'purchaseid_161'}, {'rating': '4', 'purchase_id': 'purchaseid_178'}, {'rating': '4', 'purchase_id': 'purchaseid_145'}, {'rating': '5', 'purchase_id': 'purchaseid_185'}, {'rating': '5', 'purchase_id': 'purchaseid_48'}, {'rating': '3', 'purchase_id': 'purchaseid_20'}, {'rating': '1', 'purchase_id': 'purchaseid_20'}, {'rating': '5', 'purchase_id': 'purchaseid_20'}, {'rating': '4', 'purchase_id': 'purchaseid_76'}, {'rating': '5', 'purchase_id': 'purchaseid_170'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '4', 'purchase_id': 'purchaseid_137'}, {'rating': '5', 'purchase_id': 'purchaseid_115'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '4', 'purchase_id': 'purchaseid_167'}, {'rating': '4', 'purchase_id': 'purchaseid_23'}, {'rating': '5', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'purchase_id': 'purchaseid_83'}, {'rating': '4', 'purchase_id': 'purchaseid_158'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_8'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '5', 'purchase_id': 'purchaseid_178'}, {'rating': '4', 'purchase_id': 'purchaseid_13'}, {'rating': '5', 'purchase_id': 'purchaseid_154'}, {'rating': '5', 'purchase_id': 'purchaseid_154'}, {'rating': '5', 'purchase_id': 'purchaseid_122'}, {'rating': '5', 'purchase_id': 'purchaseid_60'}, {'rating': '5', 'purchase_id': 'purchaseid_55'}, {'rating': '5', 'purchase_id': 'purchaseid_83'}, {'rating': '3', 'purchase_id': 'purchaseid_167'}, {'rating': '3', 'purchase_id': 'purchaseid_5'}, {'rating': '5', 'purchase_id': 'purchaseid_88'}, {'rating': '5', 'purchase_id': 'purchaseid_10'}, {'rating': '5', 'purchase_id': 'purchaseid_83'}, {'rating': '5', 'purchase_id': 'purchaseid_187'}, {'rating': '5', 'purchase_id': 'purchaseid_152'}, {'rating': '5', 'purchase_id': 'purchaseid_54'}, {'rating': '5', 'purchase_id': 'purchaseid_8'}, {'rating': '3', 'purchase_id': 'purchaseid_93'}, {'rating': '1', 'purchase_id': 'purchaseid_62'}, {'rating': '5', 'purchase_id': 'purchaseid_146'}, {'rating': '5', 'purchase_id': 'purchaseid_74'}, {'rating': '5', 'purchase_id': 'purchaseid_38'}, {'rating': '5', 'purchase_id': 'purchaseid_167'}, {'rating': '2', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'purchase_id': 'purchaseid_144'}]}

exec(code, env_args)
