code = """import json
import pandas as pd
import ast
import os

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
            if isinstance(first_item, dict):
                keys = list(first_item.keys())
                
                if 'book_id' in keys and 'title' in keys and 'categories' in keys:
                    books_data = data
                elif 'purchase_id' in keys and 'rating' in keys:
                    reviews_data = data
    except:
        pass

if books_data and reviews_data:
    df_books = pd.DataFrame(books_data)
    df_reviews = pd.DataFrame(reviews_data)
    
    def parse_categories(cat_str):
        if pd.isna(cat_str) or cat_str == '[]':
            return []
        try:
            return ast.literal_eval(cat_str)
        except:
            return []
    
    df_books['categories_list'] = df_books['categories'].apply(parse_categories)
    df_books_lit = df_books[df_books['categories_list'].apply(lambda x: 'Literature & Fiction' in x if x else False)]
    
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
    
    df_reviews['book_num'] = df_reviews['purchase_id'].str.extract('purchaseid_(\\d+)')
    df_books_lit['book_num'] = df_books_lit['book_id'].str.extract('bookid_(\\d+)')
    
    merged = df_books_lit.merge(df_reviews, left_on='book_num', right_on='book_num', how='inner')
    
    if not merged.empty:
        avg_ratings = merged.groupby(['book_id', 'title', 'categories']).agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        avg_ratings.columns = ['book_id', 'title', 'categories', 'avg_rating', 'review_count']
        perfect_books = avg_ratings[avg_ratings['avg_rating'] == 5.0]
        
        result = perfect_books.to_dict('records')
    else:
        result = []
else:
    result = []

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': [], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json'}

exec(code, env_args)
