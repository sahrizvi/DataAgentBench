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

# ensure details exists
if 'details' not in df_books.columns:
    df_books['details'] = ''

# extract year
pattern = re.compile(r"\b(17|18|19|20)\d{2}\b")
def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pattern.search(s)
    return int(m.group(0)) if m else None

# try from details
df_books['year_from_details'] = df_books['details'].apply(extract_year)
# try from title
df_books['year_from_title'] = df_books['title'].astype(str).apply(extract_year)
# try from categories
if 'categories' in df_books.columns:
    df_books['year_from_categories'] = df_books['categories'].astype(str).apply(extract_year)
else:
    df_books['year_from_categories'] = None

# combine
df_books['pub_year'] = df_books['year_from_details'].fillna(df_books['year_from_title']).fillna(df_books['year_from_categories'])

# counts
total = len(df_books)
have_details_year = df_books['year_from_details'].notna().sum()
have_title_year = df_books['year_from_title'].notna().sum()
have_category_year = df_books['year_from_categories'].notna().sum()
have_pub_year = df_books['pub_year'].notna().sum()

# show some examples where pub_year missing and where present
present_examples = df_books[df_books['pub_year'].notna()].head(10).to_dict(orient='records')
missing_examples = df_books[df_books['pub_year'].isna()].head(10).to_dict(orient='records')

out = {
    'total_books': total,
    'have_details_year': int(have_details_year),
    'have_title_year': int(have_title_year),
    'have_category_year': int(have_category_year),
    'have_pub_year': int(have_pub_year),
    'present_examples': present_examples,
    'missing_examples': missing_examples
}

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_4LszRktKDlz6Xx2RyChTbvWN': ['books_info'], 'var_call_6vlS6UJUOhp7xO9lN4DKuoda': ['review'], 'var_call_ywfWlhaEjWqgVCdI3tyPhrMx': 'file_storage/call_ywfWlhaEjWqgVCdI3tyPhrMx.json', 'var_call_LJElszQ2DuGKJXeywwtRzGEW': 'file_storage/call_LJElszQ2DuGKJXeywwtRzGEW.json', 'var_call_CIYSlT8y3TKUSQ35ilJGKRPz': None, 'var_call_A1SQh6Uy9B0qmiTueH87xHUS': 'file_storage/call_A1SQh6Uy9B0qmiTueH87xHUS.json', 'var_call_lw2m3pLm5EvaMoBw7HXuINzk': {'decade_stats_count': 0, 'decade_stats': [], 'eligible_count': 0, 'eligible': [], 'best': None}, 'var_call_Tu55C3JLsI7y2tzSVQvHVO1M': {'num_books_with_num': 200, 'num_reviews_with_num': 200, 'num_intersection': 200, 'intersection_sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'sample_book_nums': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'sample_review_nums': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'min_book_num': 1, 'max_book_num': 200, 'min_review_num': 1, 'max_review_num': 200}}

exec(code, env_args)
