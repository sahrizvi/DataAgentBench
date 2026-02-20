code = """import json, re
books_src = var_call_PfosPUuGQj93AMlUWgB2POIv
if isinstance(books_src, str):
    with open(books_src, 'r') as f:
        books = json.load(f)
else:
    books = books_src

year_pat = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

cnt=0
samples=[]
for r in books:
    s=str(r.get('details'))
    m=year_pat.findall(s)
    if m:
        cnt += 1
        if len(samples)<5:
            samples.append({'book_id': r.get('book_id'), 'details': s[:120], 'matches': m[:10]})

print('__RESULT__:')
print(json.dumps({'cnt_with_year_match': cnt, 'samples': samples}))"""

env_args = {'var_call_LzalIqB510Mg5NVQmMLxkmOw': 'file_storage/call_LzalIqB510Mg5NVQmMLxkmOw.json', 'var_call_EwE3Ao33qYrTv280d5AocnVc': 'file_storage/call_EwE3Ao33qYrTv280d5AocnVc.json', 'var_call_vi1Yk3ghVhrdHq3aE0UDf3TU': None, 'var_call_PfosPUuGQj93AMlUWgB2POIv': 'file_storage/call_PfosPUuGQj93AMlUWgB2POIv.json', 'var_call_OpQvfI8NiTJOzIBLlqYgULMI': None, 'var_call_WVHRwfPSD99u1svcYkv7wO9G': {'books_total': 200, 'books_with_year': 0, 'unique_book_nums': 0, 'reviews_total': 1833, 'unique_rev_nums_sample5000': 200, 'intersection_sample5000': 0}}

exec(code, env_args)
