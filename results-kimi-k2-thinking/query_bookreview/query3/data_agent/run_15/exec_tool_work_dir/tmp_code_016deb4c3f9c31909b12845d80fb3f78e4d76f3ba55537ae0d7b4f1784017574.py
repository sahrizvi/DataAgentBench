code = """import json
import re
import pandas as pd

# Load the data from files
books_file = var_functions.query_db:0
reviews_file = var_functions.query_db:5

# Read the books_data
with open(books_file, 'r') as f:
    books_data = json.load(f)

# Read the reviews_data
with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Extract numeric id for matching
books_df['book_numeric_id'] = books_df['book_id'].str.extract(r'bookid_(\d+)')
reviews_df['purchase_numeric_id'] = reviews_df['purchase_id'].str.extract(r'purchaseid_(\d+)')

# Filter for children's books
childrens_books = books_df[books_df['categories'].str.contains("Children's Books", na=False)]

# Merge with reviews using extracted numeric ids  
merged = pd.merge(
    childrens_books, 
    reviews_df, 
    left_on='book_numeric_id', 
    right_on='purchase_numeric_id', 
    how='inner'
)

# Convert rating to numeric
merged['rating'] = pd.to_numeric(merged['rating'])

# Calculate average rating per book
avg_ratings = merged.groupby(['book_id', 'title'])['rating'].mean().reset_index()

# Filter for books with average rating >= 4.5
highly_rated = avg_ratings[avg_ratings['rating'] >= 4.5]

# Sort by rating (descending) and then title
result = highly_rated.sort_values(by=['rating', 'title'], ascending=[False, True])

# Prepare the result
output = {
    'count': len(result),
    'books': result.to_dict('records')
}

print('__RESULT__:')
print(json.dumps(output, indent=2))"""

env_args = {'var_functions.query_db:0': 'file_storage/functions.query_db:0.json', 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
