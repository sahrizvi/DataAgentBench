code = """import json
import pandas as pd

# Load the data
books_file = locals()['var_functions.query_db:5']
reviews_file = locals()['var_functions.query_db:8']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Get 2020 reviews
reviews_df['review_time'] = pd.to_datetime(reviews_df['review_time'])

# Get 2020 reviews
reviews_2020 = reviews_df[reviews_df['review_time'] >= '2020-01-01'].copy()

# Extract numeric IDs
reviews_2020['review_num'] = reviews_2020['purchase_id'].str.extract('(\d+)').astype(int)
books_df['book_num'] = books_df['book_id'].str.extract('(\d+)').astype(int)

# Collect information
review_ids = reviews_2020['purchase_id'].tolist()
review_nums = reviews_2020['review_num'].tolist()
total_books = len(books_df)

# Check for matches
matches = set(reviews_2020['review_num']) & set(books_df['book_num'])
matching_nums = list(matches)

# Show all 2020 reviews
all_reviews = []
for _, review in reviews_2020.iterrows():
    book_match = books_df[books_df['book_num'] == review['review_num']]
    if not book_match.empty:
        book_title = book_match.iloc[0]['title']
    else:
        book_title = "No matching book found"
    
    all_reviews.append({
        'purchase_id': review['purchase_id'],
        'rating': review['rating'],
        'date': str(review['review_time']),
        'matching_book': book_title
    })

result = {
    'review_2020_ids': review_ids,
    'review_2020_nums': review_nums,
    'matching_book_numbers': matching_nums,
    'total_reviews_2020': len(reviews_2020),
    'review_details': all_reviews
}

print('__RESULT__:')
print(json.dumps(result, default=str))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:10': {'books_columns': ['title', 'subtitle', 'author', 'rating_number', 'features', 'description', 'price', 'store', 'categories', 'details', 'book_id'], 'reviews_columns': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id'], 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167']}, 'var_functions.execute_python:12': {'total_books': 200, 'children_books_found': 25, 'sample_children_books': ['Monstrous Stories #4: The Day the Mice Stood Still', 'The Old Man and the Pirate Princess', 'The Very Hungry Caterpillar (English and Arabic Edition)', 'Egypt (Enchantment of the World)', 'Clark the Shark: Tooth Trouble, No. 1', "I Hadn't Meant to Tell You This", 'Favorite Thorton W. Burgess Stories: 6 Books', 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'Cheer Up, Ben Franklin! (Young Historians)']}, 'var_functions.execute_python:16': {'childrens_books_found': 25, 'reviews_from_2020_onwards': 3, 'matching_review_records': 0, 'high_rated_books': []}, 'var_functions.execute_python:18': {'year_distribution': {'2012': 1, '2013': 3, '2014': 1, '2015': 1, '2019': 1, '2020': 3}, 'sample_reviews': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}, {'purchase_id': 'purchaseid_191', 'rating': '4', 'review_time': '2015-12-31 13:35:00'}, {'purchase_id': 'purchaseid_190', 'rating': '4', 'review_time': '2013-05-05 10:47:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_178', 'rating': '4', 'review_time': '2014-11-13 18:55:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-02-20 16:09:00'}, {'purchase_id': 'purchaseid_76', 'rating': '5', 'review_time': '2020-02-27 05:11:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-01-06 07:52:00'}, {'purchase_id': 'purchaseid_115', 'rating': '5', 'review_time': '2019-07-24 13:29:00'}, {'purchase_id': 'purchaseid_167', 'rating': '2', 'review_time': '2020-06-01 07:33:00'}], 'review_count': 10}, 'var_functions.execute_python:20': {'childrens_books_with_2020_reviews': [], 'other_books_with_2020_reviews': [], 'total_2020_reviews': 3}}

exec(code, env_args)
