code = """import json
import pandas as pd
import ast
import os

# Get all JSON files from /tmp
json_files = []
for root, dirs, files in os.walk('/tmp'):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

print("Found JSON files:", len(json_files))
for i, f in enumerate(json_files):
    size = os.path.getsize(f)
    print("  " + str(i) + ": " + f + " (size: " + str(size) + " bytes)")

# Try to identify which file is which based on content
books_data = None
reviews_data = None

for file_path in json_files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                keys = list(first_item.keys())
                print("\nFile " + file_path + " keys: " + str(keys))
                
                # Check if it's books data (has book_id, title, categories)
                if 'book_id' in keys and 'title' in keys and 'categories' in keys:
                    books_data = data
                    print("  -> Identified as books data")
                # Check if it's reviews data (has purchase_id, rating)
                elif 'purchase_id' in keys and 'rating' in keys:
                    reviews_data = data
                    print("  -> Identified as reviews data")
    except Exception as e:
        print("Error reading " + file_path + ": " + str(e))

if books_data is None or reviews_data is None:
    print("ERROR: Could not identify both datasets")
    books_data = []
    reviews_data = []

print("\nBooks loaded: " + str(len(books_data)))
print("Reviews loaded: " + str(len(reviews_data)))

# Create DataFrames
df_books = pd.DataFrame(books_data) if books_data else pd.DataFrame()
df_reviews = pd.DataFrame(reviews_data) if reviews_data else pd.DataFrame()

if not df_books.empty and not df_reviews.empty:
    # Show sample data
    print("\nBooks sample:")
    print(df_books[['book_id', 'title', 'categories']].head(3))
    
    print("\nReviews sample:")
    print(df_reviews[['purchase_id', 'rating']].head(3))
else:
    print("No data loaded properly")

# Filter Literature & Fiction books
if not df_books.empty:
    def parse_categories(cat_str):
        if pd.isna(cat_str) or cat_str == '[]':
            return []
        try:
            return ast.literal_eval(cat_str)
        except:
            return []
    
    df_books['categories_list'] = df_books['categories'].apply(parse_categories)
    df_books_lit = df_books[df_books['categories_list'].apply(lambda x: 'Literature & Fiction' in x if x else False)]
    print("\nLiterature & Fiction books: " + str(len(df_books_lit)))
    print(df_books_lit[['book_id', 'title']].head())
else:
    df_books_lit = pd.DataFrame()

# Process reviews if available
if not df_reviews.empty and not df_books_lit.empty:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
    
    # Extract numeric IDs for matching
    df_reviews['book_num'] = df_reviews['purchase_id'].str.extract('purchaseid_(\d+)')
    df_books_lit['book_num'] = df_books_lit['book_id'].str.extract('bookid_(\d+)')
    
    # Merge and calculate average ratings
    merged = df_books_lit.merge(df_reviews, left_on='book_num', right_on='book_num', how='inner')
    
    if not merged.empty:
        avg_ratings = merged.groupby(['book_id', 'title', 'categories']).agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        avg_ratings.columns = ['book_id', 'title', 'categories', 'avg_rating', 'review_count']
        
        # Filter for perfect 5.0 ratings
        perfect_books = avg_ratings[avg_ratings['avg_rating'] == 5.0]
        print("\nPerfect 5.0 rating books: " + str(len(perfect_books)))
        
        result = perfect_books.to_dict('records')
        print('\n__RESULT__:')
        print(json.dumps(result, indent=2))
    else:
        print("\nNo merged data found")
        print('\n__RESULT__:')
        print('[]')
else:
    print("\nMissing required data")
    print('\n__RESULT__:')
    print('[]')"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': [], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json'}

exec(code, env_args)
