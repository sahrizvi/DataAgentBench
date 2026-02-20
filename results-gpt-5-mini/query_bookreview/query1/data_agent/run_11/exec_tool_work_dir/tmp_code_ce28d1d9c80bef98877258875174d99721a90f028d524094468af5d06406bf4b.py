code = """import json
with open(var_call_fDrG1sc4I2e3ps9omdd3uqCt, 'r') as f:
    books = json.load(f)
sample = books[:10]
# prepare simplified sample
out = []
for b in sample:
    out.append({'book_id': b.get('book_id'), 'details_preview': (b.get('details') or '')[:200], 'title': b.get('title')})
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_fDrG1sc4I2e3ps9omdd3uqCt': 'file_storage/call_fDrG1sc4I2e3ps9omdd3uqCt.json', 'var_call_y8EP5NY7Cqa0I0WOjhMv4wET': 'file_storage/call_y8EP5NY7Cqa0I0WOjhMv4wET.json', 'var_call_eOXevsxizXoe8OeIplYqdnjD': {'decade': None, 'average_rating': None, 'num_books': 0}, 'var_call_MImcLFzIHXYzmFzIVvR9InOa': {'total_books_in_books_table': 200, 'books_with_extracted_year': 0, 'total_review_records': 1833, 'unique_purchase_ids_in_reviews': 200, 'unique_mapped_ids_from_reviews': 200, 'matched_books_with_reviews_and_year': 0, 'decades_all': {}}}

exec(code, env_args)
