code = """import pandas as pd
import json

# Load the book_ids from the first step
book_ids_data = json.loads(locals()['var_function-call-6989658842065073860'])
relevant_book_ids = book_ids_data['book_ids']

# Load the reviews data from the third step
with open(locals()['var_function-call-18235237849880210267'], 'r') as f:
    reviews_data = json.load(f)

df_reviews = pd.DataFrame(reviews_data)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

# Filter reviews for relevant books
df_filtered_reviews = df_reviews[df_reviews['purchase_id'].isin(relevant_book_ids)]

# Calculate average rating for each book
df_avg_ratings = df_filtered_reviews.groupby('purchase_id')['rating'].mean().reset_index()

# Identify books with a perfect average rating of 5.0
perfect_rating_book_ids = df_avg_ratings[df_avg_ratings['rating'] == 5.0]['purchase_id'].tolist()

# Load the original book information to get titles and authors
with open(locals()['var_function-call-4848310054769583768'], 'r') as f:
    books_info_data = json.load(f)

df_books_info = pd.DataFrame(books_info_data)

# Filter for books with perfect ratings and select title and author
df_result = df_books_info[df_books_info['book_id'].isin(perfect_rating_book_ids)][['title', 'author']]

# Format the output as a list of dictionaries
result = df_result.to_dict(orient='records')

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-4848310054769583768': 'file_storage/function-call-4848310054769583768.json', 'var_function-call-6989658842065073860': {'book_ids': ['bookid_1', 'bookid_9', 'bookid_13', 'bookid_30', 'bookid_36', 'bookid_37', 'bookid_38', 'bookid_39', 'bookid_44', 'bookid_49', 'bookid_55', 'bookid_69', 'bookid_70', 'bookid_74', 'bookid_77', 'bookid_82', 'bookid_84', 'bookid_89', 'bookid_92', 'bookid_93', 'bookid_98', 'bookid_99', 'bookid_101', 'bookid_106', 'bookid_109', 'bookid_111', 'bookid_122', 'bookid_137', 'bookid_142', 'bookid_144', 'bookid_161', 'bookid_167', 'bookid_171', 'bookid_177', 'bookid_179', 'bookid_180', 'bookid_182', 'bookid_187', 'bookid_188', 'bookid_195']}, 'var_function-call-18235237849880210267': 'file_storage/function-call-18235237849880210267.json'}

exec(code, env_args)
