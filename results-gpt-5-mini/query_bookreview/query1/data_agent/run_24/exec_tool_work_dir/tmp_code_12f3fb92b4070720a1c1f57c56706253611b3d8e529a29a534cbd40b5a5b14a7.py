code = """import json
import pandas as pd
import re

books_path = var_call_ywfWlhaEjWqgVCdI3tyPhrMx
reviews_path = var_call_LJElszQ2DuGKJXeywwtRzGEW

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# extract numbers
b_nums = df_books['book_id'].astype(str).str.extract(r"(\d+)")[0].dropna().astype(int).unique().tolist()
r_nums = df_reviews['purchase_id'].astype(str).str.extract(r"(\d+)")[0].dropna().astype(int).unique().tolist()

b_set = set(b_nums)
r_set = set(r_nums)
inter = sorted(list(b_set & r_set))

sample_b = sorted(b_nums)[:20]
sample_r = sorted(r_nums)[:20]

out = {
    'num_books_with_num': len(b_nums),
    'num_reviews_with_num': len(r_nums),
    'num_intersection': len(inter),
    'intersection_sample': inter[:20],
    'sample_book_nums': sample_b,
    'sample_review_nums': sample_r,
    'min_book_num': min(b_nums) if b_nums else None,
    'max_book_num': max(b_nums) if b_nums else None,
    'min_review_num': min(r_nums) if r_nums else None,
    'max_review_num': max(r_nums) if r_nums else None
}

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_4LszRktKDlz6Xx2RyChTbvWN': ['books_info'], 'var_call_6vlS6UJUOhp7xO9lN4DKuoda': ['review'], 'var_call_ywfWlhaEjWqgVCdI3tyPhrMx': 'file_storage/call_ywfWlhaEjWqgVCdI3tyPhrMx.json', 'var_call_LJElszQ2DuGKJXeywwtRzGEW': 'file_storage/call_LJElszQ2DuGKJXeywwtRzGEW.json', 'var_call_CIYSlT8y3TKUSQ35ilJGKRPz': None, 'var_call_A1SQh6Uy9B0qmiTueH87xHUS': 'file_storage/call_A1SQh6Uy9B0qmiTueH87xHUS.json', 'var_call_lw2m3pLm5EvaMoBw7HXuINzk': {'decade_stats_count': 0, 'decade_stats': [], 'eligible_count': 0, 'eligible': [], 'best': None}}

exec(code, env_args)
