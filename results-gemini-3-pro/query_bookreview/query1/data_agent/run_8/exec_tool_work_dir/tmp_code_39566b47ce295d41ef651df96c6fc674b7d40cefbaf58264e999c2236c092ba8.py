code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-13869118034911199914'], 'r') as f:
    reviews_data = json.load(f)

# Process Books
book_records = []
for b in books_data:
    bid = b.get('book_id', '')
    details = b.get('details', '')
    
    # Try regex again
    m = re.search(r'bookid_(\d+)', str(bid))
    if m:
        book_num = int(m.group(1))
        
        # Extract year
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', str(details))
        if years:
            year = int(years[0])
            book_records.append({'id': book_num, 'year': year})

df_books = pd.DataFrame(book_records)

# Process Reviews
review_records = []
for r in reviews_data:
    pid = r.get('purchase_id', '')
    rating = r.get('rating')
    
    m = re.search(r'purchaseid_(\d+)', str(pid))
    if m:
        book_num = int(m.group(1))
        try:
            val = float(rating)
            review_records.append({'id': book_num, 'rating': val})
        except:
            pass

df_reviews = pd.DataFrame(review_records)

debug_info = {}
debug_info['num_books'] = len(df_books)
debug_info['num_reviews'] = len(df_reviews)

if not df_books.empty:
    debug_info['book_ids_sample'] = df_books['id'].head(10).tolist()
    debug_info['years_sample'] = df_books['year'].head(10).tolist()

if not df_reviews.empty:
    debug_info['review_ids_sample'] = df_reviews['id'].head(10).tolist()
    book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
    book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)
    debug_info['num_books_with_ratings'] = len(book_ratings)
    
    # Merge
    df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')
    debug_info['merged_rows'] = len(df_merged)
    
    if not df_merged.empty:
        df_merged['decade'] = (df_merged['year'] // 10) * 10
        decade_stats = df_merged.groupby('decade').agg(
            num_books=('id', 'nunique'),
            avg_rating=('avg_rating', 'mean')
        ).reset_index()
        
        debug_info['decade_stats'] = decade_stats.to_dict(orient='records')
        
        qualified = decade_stats[decade_stats['num_books'] >= 10].copy()
        qualified.sort_values(by='avg_rating', ascending=False, inplace=True)
        
        if not qualified.empty:
            best_decade = qualified.iloc[0]
            result = f"{int(best_decade['decade'])}s"
        else:
            result = "None"
    else:
        result = "None"
else:
    result = "None"

print("__RESULT__:")
print(json.dumps({"result": result, "debug": debug_info}))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json', 'var_function-call-1497323203245629920': 'Done', 'var_function-call-11749323720662552993': 'None'}

exec(code, env_args)
