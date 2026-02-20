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

book_ids_with_year = 0
year_pat = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    years = [int(x) for x in year_pat.findall(str(s or ''))]
    years = [y for y in years if 1800 <= y <= 2026]
    return min(years) if years else None

book_nums=set()
for r in books:
    y=extract_year(r.get('details'))
    if y:
        book_ids_with_year += 1
        m=re.search(r'(\d+)$', str(r.get('book_id')))
        if m:
            book_nums.add(m.group(1))

rev_nums=set()
for r in reviews[:5000] if isinstance(reviews, list) else []:
    m=re.search(r'(\d+)$', str(r.get('purchase_id')))
    if m:
        rev_nums.add(m.group(1))

inter = len(book_nums & rev_nums)
res = {'books_total': len(books), 'books_with_year': book_ids_with_year, 'unique_book_nums': len(book_nums), 'reviews_total': len(reviews), 'unique_rev_nums_sample5000': len(rev_nums), 'intersection_sample5000': inter}
print('__RESULT__:')
print(json.dumps(res))"""

env_args = {'var_call_LzalIqB510Mg5NVQmMLxkmOw': 'file_storage/call_LzalIqB510Mg5NVQmMLxkmOw.json', 'var_call_EwE3Ao33qYrTv280d5AocnVc': 'file_storage/call_EwE3Ao33qYrTv280d5AocnVc.json', 'var_call_vi1Yk3ghVhrdHq3aE0UDf3TU': None, 'var_call_PfosPUuGQj93AMlUWgB2POIv': 'file_storage/call_PfosPUuGQj93AMlUWgB2POIv.json', 'var_call_OpQvfI8NiTJOzIBLlqYgULMI': None}

exec(code, env_args)
