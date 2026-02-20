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
    
    # Try finding year in details with pattern "Month DD, YYYY"
    # Matches: "released on January 1, 2004", "published ... on May 20, 1996"
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', details)
    if match:
        year = int(match.group(1))
    else:
        # Try finding year in subtitle
        match_sub = re.search(r'\d{4}', subtitle)
        if match_sub:
            year = int(match_sub.group(0))
        else:
            # Fallback: look for 4 digits in details that look like a year (e.g. 1990-2023)
            # Be careful of ISBNs. ISBNs usually don't stand alone as 4 digits.
            # Look for "published ... YYYY"
            match_broad = re.search(r'published.*?(\d{4})', details)
            if match_broad:
                year = int(match_broad.group(1))
    
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
# book_num should be string in both
merged = pd.merge(df_reviews, df_books, on='book_num', how='inner')

# Calculate decade
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Aggregation
# We need average rating per decade, considering all reviews? Or average book rating per decade?
# The query says: "Which decade of publication ... has the highest average rating ..."
# Usually this means average of all ratings for books in that decade.
# "among decades with at least 10 distinct books that have been rated"

# 1. Count distinct books per decade
decade_counts = merged.groupby('decade_str')['book_num'].nunique()

# 2. Calculate average rating per decade (average of individual review ratings)
decade_ratings = merged.groupby('decade_str')['rating'].mean()

# Combine
result_df = pd.DataFrame({'avg_rating': decade_ratings, 'book_count': decade_counts})

# Filter
filtered_df = result_df[result_df['book_count'] >= 10]

# Find max
if not filtered_df.empty:
    best_decade = filtered_df['avg_rating'].idxmax()
    best_rating = filtered_df['avg_rating'].max()
    print("__RESULT__:")
    print(json.dumps(best_decade))
else:
    print("__RESULT__:")
    print(json.dumps("No decade met the criteria"))"""

env_args = {'var_function-call-3710755877163794669': 'file_storage/function-call-3710755877163794669.json', 'var_function-call-3970585522979138389': [{'count': '200'}], 'var_function-call-14824886546566328871': [{'COUNT(*)': '1833'}], 'var_function-call-16326087428770508383': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-8708023917380946872': 'file_storage/function-call-8708023917380946872.json', 'var_function-call-17949053223017389570': 'file_storage/function-call-17949053223017389570.json'}

exec(code, env_args)
