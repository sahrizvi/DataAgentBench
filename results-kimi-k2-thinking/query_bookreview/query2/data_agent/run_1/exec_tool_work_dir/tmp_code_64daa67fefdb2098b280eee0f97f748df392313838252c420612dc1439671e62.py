code = """import json
import pandas as pd
import ast
import os

# Find and load data
json_files = []
for root, dirs, files in os.walk('/tmp'):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

books_data = None
reviews_data = None

for file_path in json_files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            keys = list(first_item.keys()) if isinstance(first_item, dict) else []
            
            if 'book_id' in keys and 'title' in keys and 'categories' in keys:
                books_data = data
            elif 'purchase_id' in keys and 'rating' in keys:
                reviews_data = data
    except:
        pass

# Check if we found data
print('Books data found:', books_data is not None)
print('Reviews data found:', reviews_data is not None)

if not books_data or not reviews_data:
    books_data = books_data if books_data else []
    reviews_data = reviews_data if reviews_data else []

df_books = pd.DataFrame(books_data) if books_data else pd.DataFrame()
df_reviews = pd.DataFrame(reviews_data) if reviews_data else pd.DataFrame()

print('Books count:', len(df_books))
print('Reviews count:', len(df_reviews))

# Show sample data
if not df_books.empty:
    print('\nBooks columns:', df_books.columns.tolist())
    print('First book:', df_books.iloc[0].to_dict())

if not df_reviews.empty:
    print('\nReviews columns:', df_reviews.columns.tolist())
    print('First review:', df_reviews.iloc[0].to_dict())

# Filter for Literature & Fiction
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
    print('\nLiterature & Fiction books count:', len(df_books_lit))

# Continue only if we have both datasets
if not df_books.empty and not df_reviews.empty and not df_books_lit.empty:
    # Clean reviews data
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
    df_reviews['book_num'] = df_reviews['purchase_id'].str.replace('purchaseid_', '')
    df_books_lit['book_num'] = df_books_lit['book_id'].str.replace('bookid_', '')
    
    print('\nReviews rating range:', df_reviews['rating'].min(), 'to', df_reviews['rating'].max())
    
    # Merge
    merged = df_books_lit.merge(df_reviews, left_on='book_num', right_on='book_num', how='inner')
    print('\nMerged records count:', len(merged))
    
    if not merged.empty:
        # Calculate average ratings per book
        avg_ratings = merged.groupby(['book_id', 'title', 'categories']).agg({
            'rating': ['mean', 'count', 'min', 'max']
        }).reset_index()
        
        avg_ratings.columns = ['book_id', 'title', 'categories', 'avg_rating', 'review_count', 'min_rating', 'max_rating']
        
        print('\nAverage ratings distribution:')
        print(avg_ratings['avg_rating'].value_counts().sort_index())
        
        # Get books with perfect 5.0 ratings
        perfect_books = avg_ratings[avg_ratings['avg_rating'] == 5.0]
        print('\nPerfect 5.0 books:', len(perfect_books))
        
        if not perfect_books.empty:
            result = perfect_books[['book_id', 'title', 'categories', 'avg_rating', 'review_count']].to_dict('records')
        else:
            # Show books with highest ratings
            top_books = avg_ratings.nlargest(5, 'avg_rating')
            print('\nTop 5 highest rated books:')
            for _, book in top_books.iterrows():
                print(f"  {book['title']}: {book['avg_rating']} ({book['review_count']} reviews)")
            result = []
    else:
        print('\nNo merged data - checking if IDs are matching correctly...')
        # Debug ID matching
        print('Book IDs sample:', df_books_lit['book_num'].unique()[:10])
        print('Review IDs sample:', df_reviews['book_num'].unique()[:10])
        result = []
else:
    result = []

print('\n__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': [], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:22': [], 'var_functions.execute_python:26': []}

exec(code, env_args)
