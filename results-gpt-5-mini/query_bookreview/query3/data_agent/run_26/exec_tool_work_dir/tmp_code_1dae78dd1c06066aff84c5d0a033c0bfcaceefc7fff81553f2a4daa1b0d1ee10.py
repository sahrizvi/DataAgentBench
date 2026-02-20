code = """import json
import re
import pandas as pd

with open(var_call_Z6VKobWBdTZKNfTkiWeWX5tN, 'r') as f:
    books = json.load(f)
with open(var_call_1f0HwMQb2lOd8NE2zfG2kTeG, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

def parse_categories(cat_str):
    try:
        if not cat_str:
            return []
        return json.loads(cat_str)
    except Exception:
        # fallback: extract quoted items
        try:
            return re.findall('"([^"]+)"', str(cat_str))
        except Exception:
            return []

df_books['categories_list'] = df_books['categories'].apply(parse_categories)

# mark children's books
def is_children_list(lst):
    for c in lst:
        if c and ("Children" in c or "Children's" in c):
            return True
    return False

df_books['is_children'] = df_books['categories_list'].apply(is_children_list)

# ratings
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# map purchaseid -> bookid
def purchase_to_bookid(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r"(\d+)$", pid)
    if m:
        return 'bookid_' + m.group(1)
    return pid.replace('purchase', 'book')

df_reviews['book_id'] = df_reviews['purchase_id'].apply(purchase_to_bookid)

# filter valid ratings
df_reviews = df_reviews[df_reviews['rating'].notna()].copy()

merged = pd.merge(df_reviews, df_books, on='book_id', how='left')
merged_children = merged[merged['is_children'] == True]

if merged_children.empty:
    output = []
else:
    group = merged_children.groupby(['book_id','title'], dropna=False).agg(
        avg_rating=('rating', 'mean'),
        review_count=('rating', 'count')
    ).reset_index()
    group['avg_rating'] = group['avg_rating'].round(3)
    res = group[group['avg_rating'] >= 4.5].sort_values(['avg_rating','review_count'], ascending=[False, False])
    output = []
    for _, row in res.iterrows():
        output.append({
            'book_id': row['book_id'],
            'title': row['title'],
            'average_rating': float(row['avg_rating']),
            'review_count': int(row['review_count'])
        })

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_Z6VKobWBdTZKNfTkiWeWX5tN': 'file_storage/call_Z6VKobWBdTZKNfTkiWeWX5tN.json', 'var_call_1f0HwMQb2lOd8NE2zfG2kTeG': 'file_storage/call_1f0HwMQb2lOd8NE2zfG2kTeG.json'}

exec(code, env_args)
