code = """import json

books_path = var_call_7FJ9IMMgIMHkvLUrf4c303HD
with open(books_path,'r',encoding='utf-8') as f:
    books = json.load(f)

sample = books[:20]
# Simplify to only book_id and details
out = [{ 'book_id': b.get('book_id'), 'details': b.get('details') } for b in sample]

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_FSwmNwxkbsM9XsVSeLxTynuU': ['books_info'], 'var_call_xNukcDXZlRQMiVAO8i7iK71g': ['review'], 'var_call_7FJ9IMMgIMHkvLUrf4c303HD': 'file_storage/call_7FJ9IMMgIMHkvLUrf4c303HD.json', 'var_call_Gj1sMenyHy1SfsivQvI5Vnz3': 'file_storage/call_Gj1sMenyHy1SfsivQvI5Vnz3.json', 'var_call_vLgNVjauTd7s2IR92nuKrtXd': None, 'var_call_20K3batRwWELXaFfVMStzZrK': {'sample_books': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20'], 'sample_reviews': ['purchaseid_1', 'purchaseid_10', 'purchaseid_100', 'purchaseid_101', 'purchaseid_102', 'purchaseid_103', 'purchaseid_104', 'purchaseid_105', 'purchaseid_106', 'purchaseid_107', 'purchaseid_108', 'purchaseid_109', 'purchaseid_11', 'purchaseid_110', 'purchaseid_111', 'purchaseid_112', 'purchaseid_113', 'purchaseid_114', 'purchaseid_115', 'purchaseid_116'], 'books_id_prefixes': {'bookid': 200}, 'reviews_id_prefixes': {'purchaseid': 200}, 'num_reviews': 200, 'num_matches_by_replace': 200}, 'var_call_beuLqTmXDjWVWchVoNgyXoyU': {'total_books_considered': 200, 'total_review_rows': 200, 'rows_with_year': 0, 'decade_stats_top20': []}}

exec(code, env_args)
