code = """import json
from pathlib import Path
import re
import pandas as pd

books_path = Path(var_call_CUdkO2yEe1cPmTYus0qHCUgo)
reviews_path = Path(var_call_x83zbwbj5mEwvUZg0hsrUepd)

books = json.load(books_path.open('r', encoding='utf-8'))
reviews = json.load(reviews_path.open('r', encoding='utf-8'))

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# extract numbers
import re

def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

books_df['num'] = books_df['book_id'].apply(extract_num)
reviews_df['num'] = reviews_df['purchase_id'].apply(extract_num)

book_nums = set(books_df['num'].dropna().astype(int).unique())
review_nums = set(reviews_df['num'].dropna().astype(int).unique())

common = sorted(list(book_nums & review_nums))

info = {
    'num_books': int(len(books_df)),
    'num_reviews': int(len(reviews_df)),
    'unique_book_nums': int(len(book_nums)),
    'unique_review_nums': int(len(review_nums)),
    'intersection_count': int(len(common)),
    'intersection_sample': common[:50]
}

# Also check if purchase ids maybe match book_id without number (full string equality)
book_ids = set(books_df['book_id'].dropna().unique())
purchase_ids = set(reviews_df['purchase_id'].dropna().unique())
full_intersection = list(book_ids & purchase_ids)
info['full_string_intersection_count'] = len(full_intersection)
info['full_string_intersection_sample'] = full_intersection[:20]

print('__RESULT__:')
print(json.dumps(info))"""

env_args = {'var_call_t8ICoTdZa5hhfV8cD7hQJlQf': ['books_info'], 'var_call_CUdkO2yEe1cPmTYus0qHCUgo': 'file_storage/call_CUdkO2yEe1cPmTYus0qHCUgo.json', 'var_call_GRCXW9zYHtaqYli2lmJg1NBh': ['review'], 'var_call_x83zbwbj5mEwvUZg0hsrUepd': 'file_storage/call_x83zbwbj5mEwvUZg0hsrUepd.json', 'var_call_pWym9YvF1umLsL0l4XXJaoQ8': {'best_decade': None, 'average_rating': None, 'book_count': 0}}

exec(code, env_args)
