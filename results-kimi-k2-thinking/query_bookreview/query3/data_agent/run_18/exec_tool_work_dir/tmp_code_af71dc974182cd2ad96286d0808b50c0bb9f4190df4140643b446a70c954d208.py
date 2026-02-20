code = """import json
import pandas as pd
import ast
from datetime import datetime

# Load the data
books_file = locals()['var_functions.query_db:5']
reviews_file = locals()['var_functions.query_db:8']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Convert review_time to datetime
reviews_df['review_time'] = pd.to_datetime(reviews_df['review_time'])

# Filter reviews from 2020 onwards
reviews_2020_onwards = reviews_df[reviews_df['review_time'] >= '2020-01-01'].copy()

# Filter for children's books
childrens_book_ids = []
for i, row in books_df.iterrows():
    try:
        cats = ast.literal_eval(row['categories'])
        if isinstance(cats, list) and any('Children' in str(cat) for cat in cats):
            childrens_book_ids.append(row['book_id'])
    except:
        pass

childrens_books_df = books_df[books_df['book_id'].isin(childrens_book_ids)].copy()

# Add numeric ids for matching
childrens_books_df['id_num'] = childrens_books_df['book_id'].str.extract('(\d+)').astype(int)
reviews_2020_onwards['id_num'] = reviews_2020_onwards['purchase_id'].str.extract('(\d+)').astype(int)

# Merge
merged_df = pd.merge(childrens_books_df, reviews_2020_onwards, on='id_num', how='inner')

# After merge, check column names
all_columns = merged_df.columns.tolist()

if len(merged_df) > 0:
    # Extract book info and ratings
    merged_df['rating'] = pd.to_numeric(merged_df['rating'], errors='coerce')
    
    # Calculate average ratings
    book_stats = merged_df.groupby(['book_id', 'title']).agg({
        'rating': ['mean', 'count']
    }).reset_index()
    
    # Flatten column names
    book_stats.columns = ['book_id', 'title', 'avg_rating', 'review_count']
    
    # Filter for high-rated books
    high_rated = book_stats[
        (book_stats['avg_rating'] >= 4.5) & 
        (book_stats['review_count'] >= 1)  # At least 1 review
    ].sort_values('avg_rating', ascending=False)
    
    result = {
        'childrens_books_found': len(childrens_book_ids),
        'reviews_from_2020_onwards': len(reviews_2020_onwards),
        'matching_review_records': len(merged_df),
        'high_rated_books': high_rated.to_dict('records') if not high_rated.empty else []
    }
else:
    result = {
        'childrens_books_found': len(childrens_book_ids),
        'reviews_from_2020_onwards': len(reviews_2020_onwards),
        'matching_review_records': 0,
        'high_rated_books': []
    }

print('__RESULT__:')
print(json.dumps(result, default=str))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:10': {'books_columns': ['title', 'subtitle', 'author', 'rating_number', 'features', 'description', 'price', 'store', 'categories', 'details', 'book_id'], 'reviews_columns': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id'], 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167']}, 'var_functions.execute_python:12': {'total_books': 200, 'children_books_found': 25, 'sample_children_books': ['Monstrous Stories #4: The Day the Mice Stood Still', 'The Old Man and the Pirate Princess', 'The Very Hungry Caterpillar (English and Arabic Edition)', 'Egypt (Enchantment of the World)', 'Clark the Shark: Tooth Trouble, No. 1', "I Hadn't Meant to Tell You This", 'Favorite Thorton W. Burgess Stories: 6 Books', 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'Cheer Up, Ben Franklin! (Young Historians)']}}

exec(code, env_args)
