code = """import json, pandas as pd, re

def load_tool_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_tool_result(var_call_evUY0EGx7A3iGYZkDSjP2UCX)
reviews = load_tool_result(var_call_Xda1sPRbicIRqmuft0SvOpV9)

df_books = pd.DataFrame(books)
df_rev = pd.DataFrame(reviews)

# Keep only true Children's Books (string contains "Children's Books")
df_books = df_books[df_books['categories'].fillna('').str.contains("Children's Books", regex=False)]

# Parse ids: bookid_123 vs purchaseid_123
book_num = df_books['book_id'].astype(str).str.extract(r'(\d+)$')[0]
df_books = df_books.assign(book_num=book_num)

rev_num = df_rev['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
df_rev = df_rev.assign(book_num=rev_num)

# Coerce rating
# rating may come as string
try:
    df_rev['rating'] = pd.to_numeric(df_rev['rating'], errors='coerce')
except Exception:
    pass

# Aggregate avg rating since 2020
agg = df_rev.dropna(subset=['book_num','rating']).groupby('book_num').agg(avg_rating=('rating','mean'), review_count=('rating','size')).reset_index()

merged = df_books.merge(agg, on='book_num', how='inner')
res = merged[merged['avg_rating']>=4.5].copy()
res = res.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = res[['title','author','book_id','avg_rating','review_count']].to_dict(orient='records')
out_json = json.dumps(out, ensure_ascii=False)
print('__RESULT__:')
print(out_json)"""

env_args = {'var_call_evUY0EGx7A3iGYZkDSjP2UCX': 'file_storage/call_evUY0EGx7A3iGYZkDSjP2UCX.json', 'var_call_Xda1sPRbicIRqmuft0SvOpV9': 'file_storage/call_Xda1sPRbicIRqmuft0SvOpV9.json'}

exec(code, env_args)
