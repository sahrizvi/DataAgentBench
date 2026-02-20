code = """import json, re
import pandas as pd

# Load reviews (may be file path)
reviews_src = var_call_MlNxuM6E5ohNqlwL2GRzTKXe
if isinstance(reviews_src, str):
    with open(reviews_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = reviews_src

details_rows = var_call_sdkpltW3UNdZX6srUZzbyzE2

# Parse publication year from details text
id_to_year = {}
for r in details_rows:
    bid = r.get('book_id')
    det = r.get('details') or ''
    m = re.search(r'\b(19\d{2}|20\d{2})\b', det)
    if m:
        id_to_year[bid] = int(m.group(1))

# Map purchaseid_x -> bookid_x (fuzzy join per hint)
pat = re.compile(r'(\d+)')

def normalize_id(s):
    if s is None:
        return None
    m = pat.search(str(s))
    return m.group(1) if m else None

# Build dataframe for reviews with matched book_id and decade
rev_df = pd.DataFrame(reviews)
if rev_df.empty:
    out = None
else:
    rev_df['num'] = rev_df['purchase_id'].map(normalize_id)
    rev_df['book_id'] = rev_df['num'].map(lambda x: f'bookid_{x}' if pd.notna(x) else None)
    rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
    rev_df = rev_df.dropna(subset=['book_id','rating'])
    rev_df['year'] = rev_df['book_id'].map(id_to_year)
    rev_df = rev_df.dropna(subset=['year'])
    rev_df['decade_start'] = (rev_df['year'] // 10) * 10
    rev_df['decade'] = rev_df['decade_start'].astype(int).astype(str) + 's'

    # distinct rated books per decade
    distinct_books = rev_df[['decade','book_id']].drop_duplicates()
    counts = distinct_books.groupby('decade').size().rename('distinct_books').reset_index()

    avg = rev_df.groupby('decade', as_index=False)['rating'].mean().rename(columns={'rating':'avg_rating'})
    summ = pd.merge(avg, counts, on='decade', how='inner')
    summ = summ[summ['distinct_books'] >= 10]
    if summ.empty:
        out = None
    else:
        best = summ.sort_values(['avg_rating','distinct_books'], ascending=[False,False]).iloc[0]
        out = {'decade': best['decade'], 'avg_rating': float(best['avg_rating']), 'distinct_books': int(best['distinct_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_sdkpltW3UNdZX6srUZzbyzE2': [{'book_id': 'bookid_47', 'details': 'The book was published on January 1, 1986, by an unspecified publisher and is written in English.'}, {'book_id': 'bookid_53', 'details': 'This book, published by Frank Amato Publications on January 1, 1997, is written in English and features a spiral binding with a total of 31 pages. It has an ISBN-10 number of 1571880879 and an ISBN-13 number of 978-1571880871. The item weighs 3.2 ounces and has dimensions of 5.5 x 0.25 x 8.75 inches.'}, {'book_id': 'bookid_54', 'details': 'This book, published by Dover Publications on August 1, 2006, is written in English and is suitable for readers aged 8 to 9 years. It has an ISBN-10 of 0486457117 and an ISBN-13 of 978-0486457116. The book weighs 1.01 pounds and has dimensions of 5.25 x 1.5 x 8.5 inches.'}, {'book_id': 'bookid_86', 'details': 'The book, published by William Stout Publishers in its first edition on January 1, 2007, is available in English and features a hardcover format with a total of 262 pages. It has an ISBN-10 of 0974621439 and an ISBN-13 of 978-0974621432. The item weighs 5.35 pounds.'}, {'book_id': 'bookid_95', 'details': 'This book is published by Tyndale House Publishers in its 14th printing edition, released on January 1, 1985. It is written in English and comes in a paperback format, comprising 240 pages. The book has an ISBN-10 of 084236661X and an ISBN-13 of 978-0842366618. Weighing 10.4 ounces, its dimensions are 5.5 inches in width, 0.75 inches in thickness, and 8.5 inches in height.'}, {'book_id': 'bookid_123', 'details': 'The book, published by Aspen Publishers on July 27, 2010, is written in English and is available in paperback format, comprising 1,232 pages. It has an ISBN-10 number of 0735590591 and an ISBN-13 number of 978-0735590595. The item weighs 3.1 pounds and has dimensions of 7 x 1.25 x 10 inches.'}, {'book_id': 'bookid_160', 'details': 'This book, published by Scala Publishers on July 12, 2006, is available in English and spans 112 pages. It has an ISBN-10 of 1857592379 and an ISBN-13 of 978-1857592375. The item weighs 1.05 pounds and its dimensions are 8.74 x 0.41 x 8.68 inches.'}, {'book_id': 'bookid_168', 'details': 'The book, published by Harcourt School Publishers in its first edition on January 1, 2008, is available in English and consists of 179 pages. It has an ISBN-10 of 015343631X and an ISBN-13 of 978-0153436314. The item weighs 13.5 ounces.'}], 'var_call_MlNxuM6E5ohNqlwL2GRzTKXe': 'file_storage/call_MlNxuM6E5ohNqlwL2GRzTKXe.json'}

exec(code, env_args)
