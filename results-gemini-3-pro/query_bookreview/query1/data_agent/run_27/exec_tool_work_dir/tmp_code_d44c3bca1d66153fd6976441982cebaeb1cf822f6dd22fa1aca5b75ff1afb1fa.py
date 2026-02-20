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
    title = b.get('title', '')
    
    year = None
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', details)
    if match:
        year = int(match.group(1))
    elif subtitle:
        match_sub = re.search(r'\d{4}', subtitle)
        if match_sub:
            year = int(match_sub.group(0))
    
    if not year:
        match_broad = re.search(r'\b(19|20)\d{2}\b', details)
        if match_broad:
            year = int(match_broad.group(0))

    if year:
        books_list.append({'book_num': book_num, 'year': year, 'title': title})

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
merged = pd.merge(df_reviews, df_books, on='book_num', how='inner')
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Inspect 1980s
df_1980s = merged[merged['decade_str'] == '1980s']
df_2020s = merged[merged['decade_str'] == '2020s']

print("__RESULT__:")
print(json.dumps({
    "1980s_books": df_1980s['title'].unique().tolist(),
    "1980s_avg": df_1980s['rating'].mean(),
    "2020s_books": df_2020s['title'].unique().tolist(),
    "2020s_avg": df_2020s['rating'].mean()
}))"""

env_args = {'var_function-call-3710755877163794669': 'file_storage/function-call-3710755877163794669.json', 'var_function-call-3970585522979138389': [{'count': '200'}], 'var_function-call-14824886546566328871': [{'COUNT(*)': '1833'}], 'var_function-call-16326087428770508383': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-8708023917380946872': 'file_storage/function-call-8708023917380946872.json', 'var_function-call-17949053223017389570': 'file_storage/function-call-17949053223017389570.json', 'var_function-call-9764193120566580812': '2020s', 'var_function-call-8437190037265893824': {'best_decade': '2020s', 'avg_rating': 4.663636363636364, 'distinct_books': 21, 'all_stats': [{'decade_str': '1880s', 'avg_rating': 4.25, 'distinct_books': 1, 'review_count': 4}, {'decade_str': '1930s', 'avg_rating': 5.0, 'distinct_books': 2, 'review_count': 3}, {'decade_str': '1940s', 'avg_rating': 5.0, 'distinct_books': 1, 'review_count': 2}, {'decade_str': '1970s', 'avg_rating': 4.285714285714286, 'distinct_books': 2, 'review_count': 7}, {'decade_str': '1980s', 'avg_rating': 4.208333333333333, 'distinct_books': 11, 'review_count': 72}, {'decade_str': '1990s', 'avg_rating': 3.8405797101449277, 'distinct_books': 18, 'review_count': 69}, {'decade_str': '2000s', 'avg_rating': 4.273684210526316, 'distinct_books': 46, 'review_count': 285}, {'decade_str': '2010s', 'avg_rating': 4.608591885441528, 'distinct_books': 88, 'review_count': 1257}, {'decade_str': '2020s', 'avg_rating': 4.663636363636364, 'distinct_books': 21, 'review_count': 110}]}, 'var_function-call-17200685279988128845': [{'decade_str': '1980s', 'avg_rating_reviews': 4.208333333333333, 'distinct_books': 11, 'avg_rating_books': 4.5481993851559075}, {'decade_str': '1990s', 'avg_rating_reviews': 3.8405797101449277, 'distinct_books': 18, 'avg_rating_books': 4.166611552028218}, {'decade_str': '2000s', 'avg_rating_reviews': 4.273684210526316, 'distinct_books': 46, 'avg_rating_books': 4.343550503205235}, {'decade_str': '2010s', 'avg_rating_reviews': 4.608591885441528, 'distinct_books': 88, 'avg_rating_books': 4.405139336568189}, {'decade_str': '2020s', 'avg_rating_reviews': 4.663636363636364, 'distinct_books': 21, 'avg_rating_books': 4.52530525030525}]}

exec(code, env_args)
