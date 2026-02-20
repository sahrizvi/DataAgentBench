code = """import json
import pandas as pd
import ast
import os
import re

# Find and load the data files
json_files = []
for root, dirs, files in os.walk('/tmp'):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

print("Found", len(json_files), "JSON files")

books_data = None
reviews_data = None

for file_path in json_files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            keys = list(first_item.keys()) if isinstance(first_item, dict) else []
            print("File keys:", keys[:5])
            
            if 'book_id' in keys and 'title' in keys:
                books_data = data
                print("Loaded books data:", len(books_data))
            elif 'purchase_id' in keys and 'rating' in keys:
                reviews_data = data
                print("Loaded reviews data:", len(reviews_data))
    except Exception as e:
        print("Error:", str(e))

# Initialize results
result = []

if books_data and reviews_data:
    df_books = pd.DataFrame(books_data)
    df_reviews = pd.DataFrame(reviews_data)
    
    print("\nBooks dataframe shape:", df_books.shape)
    print("Reviews dataframe shape:", df_reviews.shape)
    
    # Parse categories and filter for Literature & Fiction
    def parse_categories(cat_str):
        if pd.isna(cat_str) or cat_str == '[]' or not cat_str:
            return []
        try:
            return ast.literal_eval(cat_str)
        except:
            return []
    
    df_books['categories_list'] = df_books['categories'].apply(parse_categories)
    
    # Filter for Literature & Fiction category
    df_books_lit = df_books[df_books['categories_list'].apply(lambda x: 'Literature & Fiction' in x if x else False)]
    print("Literature & Fiction books:", len(df_books_lit))
    
    # Further filter for English language if details column exists
    if 'details' in df_books_lit.columns:
        df_books_lit = df_books_lit[df_books_lit['details'].str.contains('English', case=False, na=False)]
        print("English Literature & Fiction books:", len(df_books_lit))
    
    # Process reviews
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
    print("Review ratings range:", df_reviews['rating'].min(), "to", df_reviews['rating'].max())
    
    # Extract numeric IDs for matching
    df_reviews['book_num'] = df_reviews['purchase_id'].str.extract('purchaseid_(\d+)')
    df_books_lit['book_num'] = df_books_lit['book_id'].str.extract('bookid_(\d+)')
    
    # Merge books with reviews
    merged = df_books_lit.merge(df_reviews, left_on='book_num', right_on='book_num', how='inner')
    print("Merged records:", len(merged))
    
    if not merged.empty:
        # Group by book and calculate average rating
        avg_ratings = merged.groupby(['book_id', 'title', 'categories']).agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        avg_ratings.columns = ['book_id', 'title', 'categories', 'avg_rating', 'review_count']
        
        # Filter for perfect 5.0 average rating
        perfect_books = avg_ratings[avg_ratings['avg_rating'] == 5.0]
        print("Books with perfect 5.0 rating:", len(perfect_books))
        
        if not perfect_books.empty:
            # Convert to list of dicts
            result = perfect_books.to_dict('records')
        else:
            # Show books with highest ratings for debugging
            top_books = avg_ratings.nlargest(5, 'avg_rating')
            print("\nTop 5 highest rated books:")
            for _, book in top_books.iterrows():
                print(f"  {book['title']}: {book['avg_rating']} ({book['review_count']} reviews)")

print('\n__RESULT__:')
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': [], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:22': [], 'var_functions.execute_python:26': [], 'var_functions.execute_python:30': [], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json'}

exec(code, env_args)
