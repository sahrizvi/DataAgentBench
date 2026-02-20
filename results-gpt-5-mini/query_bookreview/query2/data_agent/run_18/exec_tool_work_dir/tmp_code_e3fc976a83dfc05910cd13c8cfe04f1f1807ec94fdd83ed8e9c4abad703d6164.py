code = """import json
import pandas as pd

# Load query results from storage file paths
with open(var_call_MZLw80oPzwaoG2MxSEsqkE5G, 'r') as f:
    books_json = json.load(f)
with open(var_call_y2pXQ4gXRozUXsbNlF5PeWBp, 'r') as f:
    reviews_json = json.load(f)

books_df = pd.DataFrame(books_json)
reviews_df = pd.DataFrame(reviews_json)

# Normalize reviews: convert rating to float
reviews_df['rating'] = reviews_df['rating'].astype(float)
# Map purchase_id to book_id by replacing prefix
reviews_df['book_id_mapped'] = reviews_df['purchase_id'].str.replace('purchaseid_', 'bookid_')

# Aggregate ratings per mapped book_id
agg = reviews_df.groupby('book_id_mapped').rating.agg(['mean','count']).reset_index().rename(columns={'book_id_mapped':'book_id','mean':'avg_rating','count':'review_count'})

# Filter books for English language explicitly by checking 'english' in details (case-insensitive)
books_df['details_lc'] = books_df['details'].fillna('').str.lower()
books_df['is_english'] = books_df['details_lc'].str.contains('english')

# Merge books (which were already filtered to Literature & Fiction in the SQL query) with aggregated ratings
merged = pd.merge(books_df, agg, on='book_id', how='left')

# Keep only English-language books
merged = merged[merged['is_english'] == True]

# Find books with perfect average rating of 5.0 (allow tiny float tolerance)
perfect = merged[merged['avg_rating'].notna() & (merged['avg_rating'] >= 4.9999) & (merged['avg_rating'] <= 5.0001)].copy()

# Prepare result list
result_list = []
for _, row in perfect.iterrows():
    result_list.append({
        'book_id': row['book_id'],
        'title': row.get('title'),
        'author': row.get('author'),
        'avg_rating': round(float(row['avg_rating']), 4),
        'review_count': int(row['review_count'])
    })

# Sort results by title
result_list = sorted(result_list, key=lambda x: (x['title'] or '').lower())

print("__RESULT__:")
print(json.dumps(result_list))"""

env_args = {'var_call_hhesgnPtJpok4qQtPQsakIrA': ['books_info'], 'var_call_NR0R2RaJvSYZzafImBpL4FSh': ['review'], 'var_call_MZLw80oPzwaoG2MxSEsqkE5G': 'file_storage/call_MZLw80oPzwaoG2MxSEsqkE5G.json', 'var_call_y2pXQ4gXRozUXsbNlF5PeWBp': 'file_storage/call_y2pXQ4gXRozUXsbNlF5PeWBp.json'}

exec(code, env_args)
