code = """import json
import pandas as pd

# Load query results from storage-provided variables
# var_call_BimRhIEXuOcnegIOf9CYUrzv and var_call_G4Yh8T6gc6ljRE3NRnR1XgYT

def load_var(v):
    if isinstance(v, str):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_BimRhIEXuOcnegIOf9CYUrzv)
reviews = load_var(var_call_G4Yh8T6gc6ljRE3NRnR1XgYT)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize reviews rating to numeric
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = pd.Series(dtype=float)

# Aggregate average rating per purchase_id
grp = df_reviews.groupby('purchase_id').agg(avg_rating=('rating', 'mean'), count=('rating', 'size')).reset_index()

# Map purchase_id to book_id by replacing prefix
grp['book_id'] = grp['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Select groups with perfect average rating of 5.0 (allow tiny floating tolerance)
grp_perfect = grp[grp['avg_rating'].notna() & (grp['avg_rating'].round(6) == 5.0)].copy()

# Filter books for English language and Literature & Fiction category
def has_lit_and_english(row):
    cat = row.get('categories', '')
    details = row.get('details', '')
    if not isinstance(cat, str) or not isinstance(details, str):
        return False
    return ('Literature & Fiction' in cat) and ('English' in details)

if not df_books.empty:
    df_books['matches'] = df_books.apply(has_lit_and_english, axis=1)
    df_books_filtered = df_books[df_books['matches'] == True].copy()
else:
    df_books_filtered = df_books.copy()

# Merge perfect-rated groups with filtered books on book_id
merged = pd.merge(grp_perfect, df_books_filtered, on='book_id', how='inner')

# Prepare final result list
result = []
for _, r in merged.iterrows():
    result.append({
        'book_id': r.get('book_id'),
        'title': r.get('title'),
        'author': r.get('author'),
        'avg_rating': float(r.get('avg_rating')) if pd.notna(r.get('avg_rating')) else None,
        'review_count': int(r.get('count')) if pd.notna(r.get('count')) else 0
    })

# Ensure JSON serializable
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_fQJ43iL9WRBrzYH151dwck8J': ['books_info'], 'var_call_BimRhIEXuOcnegIOf9CYUrzv': 'file_storage/call_BimRhIEXuOcnegIOf9CYUrzv.json', 'var_call_h2NXKvYEWzdhYXATgXeYdkyk': ['review'], 'var_call_G4Yh8T6gc6ljRE3NRnR1XgYT': 'file_storage/call_G4Yh8T6gc6ljRE3NRnR1XgYT.json'}

exec(code, env_args)
