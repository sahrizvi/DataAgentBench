code = """import json, re, pandas as pd

books_src = var_call_PfosPUuGQj93AMlUWgB2POIv
if isinstance(books_src, str):
    with open(books_src, 'r') as f:
        books = json.load(f)
else:
    books = books_src

reviews_src = var_call_EwE3Ao33qYrTv280d5AocnVc
if isinstance(reviews_src, str):
    with open(reviews_src, 'r') as f:
        reviews = json.load(f)
else:
    reviews = reviews_src

year_pat = re.compile(r'(?<!\d)(18\d{2}|19\d{2}|20\d{2})(?!\d)')

def extract_year(s):
    years = [int(x) for x in year_pat.findall(str(s or ''))]
    years = [y for y in years if 1800 <= y <= 2026]
    return min(years) if years else None

book_rows=[]
for r in books:
    bid=r.get('book_id')
    y=extract_year(r.get('details'))
    if bid and y:
        book_rows.append({'book_id': str(bid), 'year': y})

books_df=pd.DataFrame(book_rows)
if books_df.empty:
    result=None
else:
    books_df=books_df.drop_duplicates('book_id')
    num_pat=re.compile(r'(\d+)$')
    def suffix_num(x):
        m=num_pat.search(str(x))
        return m.group(1) if m else None
    books_df['num']=books_df['book_id'].map(suffix_num)

    rev_df=pd.DataFrame(reviews)
    rev_df=rev_df.dropna(subset=['purchase_id','rating'])
    rev_df['rating']=pd.to_numeric(rev_df['rating'], errors='coerce')
    rev_df=rev_df.dropna(subset=['rating'])
    rev_df['num']=rev_df['purchase_id'].map(suffix_num)

    joined=rev_df.merge(books_df[['book_id','year','num']], on='num', how='inner')
    joined['decade_start']=(joined['year']//10)*10
    joined['decade']=joined['decade_start'].astype(int).astype(str)+'s'
    agg=joined.groupby('decade').agg(distinct_books=('book_id','nunique'), avg_rating=('rating','mean')).reset_index()
    agg=agg[agg['distinct_books']>=10]
    if agg.empty:
        result=None
    else:
        best=agg.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
        result={'decade': best['decade'], 'avg_rating': float(best['avg_rating']), 'distinct_books': int(best['distinct_books'])}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_LzalIqB510Mg5NVQmMLxkmOw': 'file_storage/call_LzalIqB510Mg5NVQmMLxkmOw.json', 'var_call_EwE3Ao33qYrTv280d5AocnVc': 'file_storage/call_EwE3Ao33qYrTv280d5AocnVc.json', 'var_call_vi1Yk3ghVhrdHq3aE0UDf3TU': None, 'var_call_PfosPUuGQj93AMlUWgB2POIv': 'file_storage/call_PfosPUuGQj93AMlUWgB2POIv.json', 'var_call_OpQvfI8NiTJOzIBLlqYgULMI': None, 'var_call_WVHRwfPSD99u1svcYkv7wO9G': {'books_total': 200, 'books_with_year': 0, 'unique_book_nums': 0, 'reviews_total': 1833, 'unique_rev_nums_sample5000': 200, 'intersection_sample5000': 0}, 'var_call_VhDIxv6q8w7rMrfTMoX2lz7R': {'cnt_with_year_match': 0, 'samples': []}, 'var_call_6jZj7UueTwjN4vQW9ZJiWUjT': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}], 'var_call_j23Ak75XTBfRJlbAtSXzIuJj': {'matches': []}, 'var_call_DzSjZ5cO4BqejtKUOb3OQ7Tb': {'m': ['2004'], 'm2': ['2004']}, 'var_call_pw5DMmGd8Ob8ZvMbInEhZZcN': {'matches': [], 'repr': "'... 2004.'"}, 'var_call_Q5IHa007Bq2ieccJAVJDXZa5': {'findall': ['2004'], 'search': True, 'parts': ['.', '.', '.', ' ', '2', '0', '0', '4', '.']}, 'var_call_c00ELJm8NrUNp6dYFeogZ7N7': {'findall': [], 'search': None}, 'var_call_f5IqQFKKPDndy9JiiFQryL8g': {'m': ['2004'], 'm2': ['2004'], 'm3': ['2004']}, 'var_call_C7n81ChxkeVRSXZMWpwlKVdX': {'pattern': '\x08(18\\d{2}|19\\d{2}|20\\d{2})\x08'}}

exec(code, env_args)
