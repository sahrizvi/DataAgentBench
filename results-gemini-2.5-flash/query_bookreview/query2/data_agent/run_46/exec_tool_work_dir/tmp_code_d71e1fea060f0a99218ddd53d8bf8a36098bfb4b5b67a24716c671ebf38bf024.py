code = """import json
import pandas as pd

books_data_path = locals()['var_function-call-1912753410291148554']
with open(books_data_path, 'r') as f:
    books_info = json.load(f)

reviews_data_path = locals()['var_function-call-16317400724596862313']
with open(reviews_data_path, 'r') as f:
    reviews_info = json.load(f)

books_df = pd.DataFrame(books_info)
reviews_df = pd.DataFrame(reviews_info)

# Filter for English-language books in 'Literature & Fiction' category
filtered_books = []
for index, row in books_df.iterrows():
    categories = row['categories']
    details = row['details']
    
    if isinstance(categories, str):
        if 'Literature & Fiction' in categories and 'English' in details:
            filtered_books.append(row)

filtered_books_df = pd.DataFrame(filtered_books)

# Convert rating to float for aggregation
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Merge and find average rating
merged_df = pd.merge(filtered_books_df, reviews_df, left_on='book_id', right_on='purchase_id', how='inner')

average_ratings = merged_df.groupby('book_id')['rating'].mean().reset_index()

# Find books with a perfect 5.0 rating
perfect_rating_books = average_ratings[average_ratings['rating'] == 5.0]

# Get the titles of these books
final_books = pd.merge(perfect_rating_books, books_df, on='book_id', how='inner')
result_titles = final_books['title'].tolist()

print("__RESULT__:")
print(json.dumps(result_titles))"""

env_args = {'var_function-call-5108956238972008348': [], 'var_function-call-4891174312442297353': 'file_storage/function-call-4891174312442297353.json', 'var_function-call-6280416549282027771': 'file_storage/function-call-6280416549282027771.json', 'var_function-call-16317400724596862313': 'file_storage/function-call-16317400724596862313.json', 'var_function-call-3227518443145659596': [], 'var_function-call-1912753410291148554': 'file_storage/function-call-1912753410291148554.json'}

exec(code, env_args)
