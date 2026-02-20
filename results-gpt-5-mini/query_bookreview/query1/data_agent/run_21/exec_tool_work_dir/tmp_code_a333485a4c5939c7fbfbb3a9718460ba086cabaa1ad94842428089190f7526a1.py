code = """import json
import pandas as pd

books_path = var_call_7FJ9IMMgIMHkvLUrf4c303HD
reviews_path = var_call_Gj1sMenyHy1SfsivQvI5Vnz3

with open(books_path,'r',encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path,'r',encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# show sample ids and counts
sample_books = books_df['book_id'].head(20).tolist()
sample_reviews = reviews_df['purchase_id'].head(20).tolist()

books_id_prefixes = books_df['book_id'].astype(str).str.extract(r'(^[^_]+)')[0].value_counts().to_dict()
reviews_id_prefixes = reviews_df['purchase_id'].astype(str).str.extract(r'(^[^_]+)')[0].value_counts().to_dict()

# Count how many purchase_ids map to a corresponding book_id by simple replace
mapped = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_','bookid_')
matches = mapped.isin(books_df['book_id'])
num_matches = int(matches.sum())
num_reviews = len(reviews_df)

out = {
    'sample_books': sample_books,
    'sample_reviews': sample_reviews,
    'books_id_prefixes': books_id_prefixes,
    'reviews_id_prefixes': reviews_id_prefixes,
    'num_reviews': num_reviews,
    'num_matches_by_replace': num_matches
}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_FSwmNwxkbsM9XsVSeLxTynuU': ['books_info'], 'var_call_xNukcDXZlRQMiVAO8i7iK71g': ['review'], 'var_call_7FJ9IMMgIMHkvLUrf4c303HD': 'file_storage/call_7FJ9IMMgIMHkvLUrf4c303HD.json', 'var_call_Gj1sMenyHy1SfsivQvI5Vnz3': 'file_storage/call_Gj1sMenyHy1SfsivQvI5Vnz3.json', 'var_call_vLgNVjauTd7s2IR92nuKrtXd': None}

exec(code, env_args)
