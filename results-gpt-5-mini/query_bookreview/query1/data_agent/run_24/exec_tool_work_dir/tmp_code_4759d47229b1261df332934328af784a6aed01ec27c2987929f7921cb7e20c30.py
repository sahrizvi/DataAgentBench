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

# Extract numeric id
df_books['book_num'] = df_books['book_id'].astype(str).str.extract(r"(\d+)")
df_reviews['book_num'] = df_reviews['purchase_id'].astype(str).str.extract(r"(\d+)")

# Drop missing
df_books = df_books[df_books['book_num'].notna()].copy()
df_reviews = df_reviews[df_reviews['book_num'].notna()].copy()

df_books['book_num'] = df_books['book_num'].astype(int)
df_reviews['book_num'] = df_reviews['book_num'].astype(int)

# Extract pub year
def extract_year(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"\b(17|18|19|20)\d{2}\b", s)
    if m:
        return int(m.group(0))
    return None

if 'details' not in df_books.columns:
    df_books['details'] = ''

df_books['pub_year'] = df_books['details'].apply(extract_year)
# Some books may have year in title or elsewhere; try searching title
no_year = df_books['pub_year'].isna()
if no_year.any():
    df_books.loc[no_year, 'pub_year'] = df_books.loc[no_year, 'title'].astype(str).apply(extract_year)

# Drop without year
df_books = df_books[df_books['pub_year'].notna()].copy()

def year_to_decade(y):
    y = int(y)
    decade = (y // 10) * 10
    return f"{decade}s"

df_books['decade'] = df_books['pub_year'].apply(year_to_decade)

# Clean ratings
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews[df_reviews['rating'].notna()].copy()

merged = pd.merge(df_reviews, df_books, on='book_num', how='inner', suffixes=('_rev','_book'))

per_book = merged.groupby(['book_num','book_id','decade'], as_index=False)['rating'].mean().rename(columns={'rating':'avg_rating'})

decade_stats = per_book.groupby('decade').agg(num_books=('book_id','nunique'), mean_of_book_avgs=('avg_rating','mean')).reset_index()

decade_stats = decade_stats.sort_values('num_books', ascending=False)

eligible = decade_stats[decade_stats['num_books'] >= 10].sort_values('mean_of_book_avgs', ascending=False)

# Prepare serializable output
decade_list = decade_stats.to_dict(orient='records')
eligible_list = eligible.to_dict(orient='records')

best = None
if len(eligible_list) > 0:
    best_row = eligible.iloc[0]
    best = {'decade': best_row['decade'], 'average_rating': round(float(best_row['mean_of_book_avgs']),4), 'num_books': int(best_row['num_books'])}

output = {
    'decade_stats_count': len(decade_list),
    'decade_stats': decade_list,
    'eligible_count': len(eligible_list),
    'eligible': eligible_list,
    'best': best
}

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_4LszRktKDlz6Xx2RyChTbvWN': ['books_info'], 'var_call_6vlS6UJUOhp7xO9lN4DKuoda': ['review'], 'var_call_ywfWlhaEjWqgVCdI3tyPhrMx': 'file_storage/call_ywfWlhaEjWqgVCdI3tyPhrMx.json', 'var_call_LJElszQ2DuGKJXeywwtRzGEW': 'file_storage/call_LJElszQ2DuGKJXeywwtRzGEW.json', 'var_call_CIYSlT8y3TKUSQ35ilJGKRPz': None, 'var_call_A1SQh6Uy9B0qmiTueH87xHUS': 'file_storage/call_A1SQh6Uy9B0qmiTueH87xHUS.json'}

exec(code, env_args)
