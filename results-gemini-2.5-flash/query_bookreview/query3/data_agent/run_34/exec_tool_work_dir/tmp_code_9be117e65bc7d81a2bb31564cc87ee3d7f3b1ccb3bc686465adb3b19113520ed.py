code = """import pandas as pd
import json

# Extract the JSON string from the query_db result
raw_childrens_books_string = locals()['var_function-call-5007990040283121851']['results'][0]

# Find the index where the actual JSON array starts
json_start_index = raw_childrens_books_string.find('[')
json_end_index = raw_childrens_books_string.rfind(']') + 1 # Include the closing bracket

childrens_books_json_str = raw_childrens_books_string[json_start_index:json_end_index]
childrens_books_data = json.loads(childrens_books_json_str)
childrens_books_ids = [book['book_id'] for book in childrens_books_data]

# Load reviews data from the file
with open(locals()['var_function-call-7857881015001238920'], 'r') as f:
    reviews_data = json.load(f)

reviews_df = pd.DataFrame(reviews_data)
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'])
reviews_df['review_year'] = pd.to_datetime(reviews_df['review_time']).dt.year

# Filter reviews from 2020 onwards
reviews_2020_onwards = reviews_df[reviews_df['review_year'] >= 2020]

# Filter reviews for Children's Books
childrens_reviews = reviews_2020_onwards[reviews_2020_onwards['purchase_id'].isin(childrens_books_ids)]

# Calculate average rating for each book
avg_ratings = childrens_reviews.groupby('purchase_id')['rating'].mean().reset_index()

# Filter books with an average rating of at least 4.5
highly_rated_childrens_books = avg_ratings[avg_ratings['rating'] >= 4.5]

print("__RESULT__:")
print(highly_rated_childrens_books.to_json(orient='records'))"""

env_args = {'var_function-call-10271262895857587966': ['books_info'], 'var_function-call-5007990040283121851': [{'book_id': 'bookid_4'}, {'book_id': 'bookid_14'}, {'book_id': 'bookid_32'}, {'book_id': 'bookid_40'}, {'book_id': 'bookid_48'}, {'book_id': 'bookid_52'}, {'book_id': 'bookid_54'}, {'book_id': 'bookid_55'}, {'book_id': 'bookid_57'}, {'book_id': 'bookid_96'}, {'book_id': 'bookid_99'}, {'book_id': 'bookid_108'}, {'book_id': 'bookid_111'}, {'book_id': 'bookid_116'}, {'book_id': 'bookid_120'}, {'book_id': 'bookid_124'}, {'book_id': 'bookid_130'}, {'book_id': 'bookid_132'}, {'book_id': 'bookid_145'}, {'book_id': 'bookid_146'}, {'book_id': 'bookid_149'}, {'book_id': 'bookid_152'}, {'book_id': 'bookid_158'}, {'book_id': 'bookid_163'}, {'book_id': 'bookid_170'}], 'var_function-call-7857881015001238920': 'file_storage/function-call-7857881015001238920.json'}

exec(code, env_args)
