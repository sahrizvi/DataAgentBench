code = """import json, re
with open(var_call_fCXKjFuQR0KVnKs5USPd527y,'r',encoding='utf-8') as f:
    books = json.load(f)
pattern = re.compile(r'(18\d{2}|19\d{2}|20\d{2})')
res = []
count = 0
for b in books[:200]:
    d = b.get('details','')
    m = pattern.findall(d if isinstance(d,str) else '')
    years = sorted(set(m))
    res.append({'book_id': b.get('book_id'), 'years_found': years})
    if years:
        count += 1

out = {'sample': res[:50], 'books_with_year_count': count}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_igXNZFokW0Vgy87s2Yc02xki': ['books_info'], 'var_call_WvRkgUDcO28qseDky23cQ2B6': ['review'], 'var_call_fCXKjFuQR0KVnKs5USPd527y': 'file_storage/call_fCXKjFuQR0KVnKs5USPd527y.json', 'var_call_0WiZXUQS5sLYvZ5ccFLAWezZ': 'file_storage/call_0WiZXUQS5sLYvZ5ccFLAWezZ.json', 'var_call_aR6UX9hpPPFJp9mKhHqshRo4': {'error': 'No matched reviews and books after fuzzy numeric id join.'}, 'var_call_kZWI5G5YvvZNgvtJ34upADAx': {'books_total': 200, 'reviews_total': 1833, 'books_with_num': 200, 'reviews_with_num': 200, 'books_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'reviews_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'intersection_count': 200, 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_76', 'purchaseid_115', 'purchaseid_167', 'purchaseid_188', 'purchaseid_23', 'purchaseid_196', 'purchaseid_3', 'purchaseid_48', 'purchaseid_154', 'purchaseid_99', 'purchaseid_169', 'purchaseid_145', 'purchaseid_194', 'purchaseid_81', 'purchaseid_199']}, 'var_call_tZT56yqXTJfyWBmH174CmQyu': {'error': 'No matched reviews and books after join.'}, 'var_call_VVrmJaDl400FEdaox2BPvYVq': {'total_books': 200, 'books_with_year_count': 0, 'books_with_year_sample_ids': [], 'books_with_year_id_nums_sample': [], 'total_reviews': 1833, 'reviews_id_nums_sample': ['186', '191', '190', '8', '178', '76', '115', '167', '188', '23', '196', '3', '48', '154', '99', '169', '145', '194', '81', '199'], 'intersection_id_nums_count': 0}, 'var_call_iwBj8ZLRGYPRVbQUAO30M7xd': 'file_storage/call_iwBj8ZLRGYPRVbQUAO30M7xd.json'}

exec(code, env_args)
