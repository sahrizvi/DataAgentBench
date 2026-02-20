code = """import json
import pandas as pd
import ast

# Load the data
books_file = locals()['var_functions.query_db:5']
reviews_file = locals()['var_functions.query_db:8']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Filter reviews from 2020 onwards
reviews_df['review_time'] = pd.to_datetime(reviews_df['review_time'])
reviews_2020 = reviews_df[reviews_df['review_time'] >= '2020-01-01'].copy()

# Extract numeric IDs for matching
reviews_2020['id_num'] = reviews_2020['purchase_id'].str.extract('(\d+)').astype(int)
books_df['id_num'] = books_df['book_id'].str.extract('(\d+)').astype(int)

# Merge to find which books have 2020 reviews
merged_2020 = pd.merge(books_df, reviews_2020, on='id_num', how='inner')

# Check which 2020 reviews exist
review_2020_ids = reviews_2020['id_num'].tolist()

# Check categories for these books
childrens_books_with_2020_reviews = []
other_books_with_2020_reviews = []

for _, row in merged_2020.iterrows():
    try:
        cats = ast.literal_eval(row['categories'])
        is_children = any('Children' in str(cat) for cat in cats)
        
        book_info = {
            'book_id': row['book_id'],
            'title': row['title'],
            'categories': cats,
            'avg_rating': float(row['rating']),
            'review_time': str(row['review_time'])
        }
        
        if is_children:
            childrens_books_with_2020_reviews.append(book_info)
        else:
            other_books_with_2020_reviews.append(book_info)
    except:
        pass

result = {
    'childrens_books_with_2020_reviews': childrens_books_with_2020_reviews,
    'other_books_with_2020_reviews': other_books_with_2020_reviews,
    'total_2020_reviews': len(reviews_2020)
}

print('__RESULT__:')
print(json.dumps(result, default=str))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:10': {'books_columns': ['title', 'subtitle', 'author', 'rating_number', 'features', 'description', 'price', 'store', 'categories', 'details', 'book_id'], 'reviews_columns': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id'], 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167']}, 'var_functions.execute_python:12': {'total_books': 200, 'children_books_found': 25, 'sample_children_books': ['Monstrous Stories #4: The Day the Mice Stood Still', 'The Old Man and the Pirate Princess', 'The Very Hungry Caterpillar (English and Arabic Edition)', 'Egypt (Enchantment of the World)', 'Clark the Shark: Tooth Trouble, No. 1', "I Hadn't Meant to Tell You This", 'Favorite Thorton W. Burgess Stories: 6 Books', 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'Cheer Up, Ben Franklin! (Young Historians)']}, 'var_functions.execute_python:16': {'childrens_books_found': 25, 'reviews_from_2020_onwards': 3, 'matching_review_records': 0, 'high_rated_books': []}, 'var_functions.execute_python:18': {'year_distribution': {'2012': 1, '2013': 3, '2014': 1, '2015': 1, '2019': 1, '2020': 3}, 'sample_reviews': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}, {'purchase_id': 'purchaseid_191', 'rating': '4', 'review_time': '2015-12-31 13:35:00'}, {'purchase_id': 'purchaseid_190', 'rating': '4', 'review_time': '2013-05-05 10:47:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_178', 'rating': '4', 'review_time': '2014-11-13 18:55:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-02-20 16:09:00'}, {'purchase_id': 'purchaseid_76', 'rating': '5', 'review_time': '2020-02-27 05:11:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-01-06 07:52:00'}, {'purchase_id': 'purchaseid_115', 'rating': '5', 'review_time': '2019-07-24 13:29:00'}, {'purchase_id': 'purchaseid_167', 'rating': '2', 'review_time': '2020-06-01 07:33:00'}], 'review_count': 10}}

exec(code, env_args)
