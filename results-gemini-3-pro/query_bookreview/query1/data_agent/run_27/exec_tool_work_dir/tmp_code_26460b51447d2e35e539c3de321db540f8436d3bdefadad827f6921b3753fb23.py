code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-8708023917380946872'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-17949053223017389570'], 'r') as f:
    reviews_data = json.load(f)

# Process books
books_list = []
for b in books_data:
    book_id = b['book_id']
    book_num = book_id.replace('bookid_', '')
    details = b.get('details', '')
    subtitle = b.get('subtitle', '')
    
    year = None
    # Regex for "Month DD, YYYY"
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', details)
    if match:
        year = int(match.group(1))
    elif subtitle:
        match_sub = re.search(r'\d{4}', subtitle)
        if match_sub:
            year = int(match_sub.group(0))
    
    if not year:
        # Fallback to finding just 4 digits in details
        match_broad = re.search(r'\b(19|20)\d{2}\b', details)
        if match_broad:
            year = int(match_broad.group(0))

    if year:
        books_list.append({'book_num': book_num, 'year': year})

df_books = pd.DataFrame(books_list)

# Process reviews
reviews_list = []
for r in reviews_data:
    purchase_id = r['purchase_id']
    book_num = purchase_id.replace('purchaseid_', '')
    rating = float(r['rating'])
    reviews_list.append({'book_num': book_num, 'rating': rating})

df_reviews = pd.DataFrame(reviews_list)

# Merge
# Ensure book_num is same type
merged = pd.merge(df_reviews, df_books, on='book_num', how='inner')

# Calculate decade
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Aggregation 1: Average of all ratings
decade_stats = merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    distinct_books=('book_num', 'nunique'),
    review_count=('rating', 'count')
).reset_index()

# Filter
filtered = decade_stats[decade_stats['distinct_books'] >= 10]

# Sort by avg_rating
best_decade = filtered.sort_values('avg_rating', ascending=False).iloc[0]

print("__RESULT__:")
print(json.dumps({
    "best_decade": best_decade['decade_str'],
    "avg_rating": best_decade['avg_rating'],
    "distinct_books": int(best_decade['distinct_books']),
    "all_stats": decade_stats.to_dict(orient='records')
}))"""

env_args = {'var_function-call-3710755877163794669': 'file_storage/function-call-3710755877163794669.json', 'var_function-call-3970585522979138389': [{'count': '200'}], 'var_function-call-14824886546566328871': [{'COUNT(*)': '1833'}], 'var_function-call-16326087428770508383': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-8708023917380946872': 'file_storage/function-call-8708023917380946872.json', 'var_function-call-17949053223017389570': 'file_storage/function-call-17949053223017389570.json', 'var_function-call-9764193120566580812': '2020s'}

exec(code, env_args)
