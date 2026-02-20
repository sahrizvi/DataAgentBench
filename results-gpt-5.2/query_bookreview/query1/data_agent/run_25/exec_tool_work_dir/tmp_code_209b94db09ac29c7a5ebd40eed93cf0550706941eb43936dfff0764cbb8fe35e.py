code = """import json, re
import pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_36znDMBtOkeNr9riqxGiO73s)
reviews = load_records(var_call_5EZpQJjRpjY83aPPrihDAjyi)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# extract year
year_pat = re.compile(r'\b(\d{4})\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    years = [int(y) for y in year_pat.findall(text)]
    years = [y for y in years if 1500 <= y <= 2026]
    return years[0] if years else None

bdf['year'] = bdf['details'].apply(extract_year)
bdf['key'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]

rdf['key'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['key','rating'])

books_with_year = bdf.dropna(subset=['year','key'])['key'].nunique()
books_total = bdf['key'].nunique()
review_keys = rdf['key'].nunique()
joined = rdf.merge(bdf.dropna(subset=['year'])[['key','year']], on='key', how='inner')
joined_keys = joined['key'].nunique()

print('__RESULT__:')
print(json.dumps({
    'books_total': int(books_total),
    'books_with_year': int(books_with_year),
    'review_distinct_books': int(review_keys),
    'joined_distinct_books': int(joined_keys),
    'joined_rows': int(len(joined))
}))"""

env_args = {'var_call_nuWYADeHCSdr0FMNeOqFkvJt': 'file_storage/call_nuWYADeHCSdr0FMNeOqFkvJt.json', 'var_call_5EZpQJjRpjY83aPPrihDAjyi': 'file_storage/call_5EZpQJjRpjY83aPPrihDAjyi.json', 'var_call_jWREfBZxjbuos3PeCJPKppLu': {'decade': None}, 'var_call_36znDMBtOkeNr9riqxGiO73s': 'file_storage/call_36znDMBtOkeNr9riqxGiO73s.json', 'var_call_MdIxdtORht2besMrBcKvlTvN': {'top': {'decade': None, 'note': 'No decade has >=10 distinct rated books after join.'}, 'eligible': [], 'all': []}, 'var_call_dWRS7wISMJWAQLGKvcYeJ24k': [{'purchase_id': 'purchaseid_196', 'n_reviews': '194'}, {'purchase_id': 'purchaseid_8', 'n_reviews': '190'}, {'purchase_id': 'purchaseid_3', 'n_reviews': '146'}, {'purchase_id': 'purchaseid_178', 'n_reviews': '118'}, {'purchase_id': 'purchaseid_186', 'n_reviews': '80'}, {'purchase_id': 'purchaseid_20', 'n_reviews': '42'}, {'purchase_id': 'purchaseid_10', 'n_reviews': '40'}, {'purchase_id': 'purchaseid_145', 'n_reviews': '36'}, {'purchase_id': 'purchaseid_190', 'n_reviews': '34'}, {'purchase_id': 'purchaseid_154', 'n_reviews': '29'}, {'purchase_id': 'purchaseid_148', 'n_reviews': '29'}, {'purchase_id': 'purchaseid_48', 'n_reviews': '27'}, {'purchase_id': 'purchaseid_5', 'n_reviews': '25'}, {'purchase_id': 'purchaseid_158', 'n_reviews': '24'}, {'purchase_id': 'purchaseid_95', 'n_reviews': '23'}, {'purchase_id': 'purchaseid_62', 'n_reviews': '22'}, {'purchase_id': 'purchaseid_165', 'n_reviews': '22'}, {'purchase_id': 'purchaseid_99', 'n_reviews': '20'}, {'purchase_id': 'purchaseid_72', 'n_reviews': '19'}, {'purchase_id': 'purchaseid_89', 'n_reviews': '18'}], 'var_call_RCgwe3hhFIJ5aFFmBaK6XQtj': [{'n_books': '200', 'max_suffix': '200'}]}

exec(code, env_args)
