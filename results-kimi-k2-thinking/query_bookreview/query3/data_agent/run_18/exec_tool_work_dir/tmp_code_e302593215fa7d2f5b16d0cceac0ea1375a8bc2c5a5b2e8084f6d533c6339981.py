code = """import json
import pandas as pd

# Load the data
reviews_file = locals()['var_functions.query_db:8']

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

reviews_df = pd.DataFrame(reviews_data)

# Check review years available
reviews_df['review_time'] = pd.to_datetime(reviews_df['review_time'])
reviews_df['year'] = reviews_df['review_time'].dt.year

year_counts = reviews_df['year'].value_counts().sort_index()

# Show all reviews
all_reviews = reviews_df[['purchase_id', 'rating', 'review_time']].head(20)

result = {
    'year_distribution': year_counts.to_dict(),
    'sample_reviews': all_reviews.to_dict('records'),
    'review_count': len(reviews_df)
}

print('__RESULT__:')
print(json.dumps(result, default=str))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:10': {'books_columns': ['title', 'subtitle', 'author', 'rating_number', 'features', 'description', 'price', 'store', 'categories', 'details', 'book_id'], 'reviews_columns': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id'], 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167']}, 'var_functions.execute_python:12': {'total_books': 200, 'children_books_found': 25, 'sample_children_books': ['Monstrous Stories #4: The Day the Mice Stood Still', 'The Old Man and the Pirate Princess', 'The Very Hungry Caterpillar (English and Arabic Edition)', 'Egypt (Enchantment of the World)', 'Clark the Shark: Tooth Trouble, No. 1', "I Hadn't Meant to Tell You This", 'Favorite Thorton W. Burgess Stories: 6 Books', 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'Cheer Up, Ben Franklin! (Young Historians)']}, 'var_functions.execute_python:16': {'childrens_books_found': 25, 'reviews_from_2020_onwards': 3, 'matching_review_records': 0, 'high_rated_books': []}}

exec(code, env_args)
