code = """import json
from pathlib import Path
books_path = Path(var_call_CUdkO2yEe1cPmTYus0qHCUgo)
books = json.load(books_path.open('r', encoding='utf-8'))
sample = []
for i, b in enumerate(books[:40]):
    sample.append({'i': i, 'book_id': b.get('book_id'), 'details': b.get('details')})

print('__RESULT__:')
print(json.dumps(sample))"""

env_args = {'var_call_t8ICoTdZa5hhfV8cD7hQJlQf': ['books_info'], 'var_call_CUdkO2yEe1cPmTYus0qHCUgo': 'file_storage/call_CUdkO2yEe1cPmTYus0qHCUgo.json', 'var_call_GRCXW9zYHtaqYli2lmJg1NBh': ['review'], 'var_call_x83zbwbj5mEwvUZg0hsrUepd': 'file_storage/call_x83zbwbj5mEwvUZg0hsrUepd.json', 'var_call_pWym9YvF1umLsL0l4XXJaoQ8': {'best_decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_ZmhAUewJuPHzFH1v3EarTie1': {'num_books': 200, 'num_reviews': 1833, 'unique_book_nums': 200, 'unique_review_nums': 200, 'intersection_count': 200, 'intersection_sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 'full_string_intersection_count': 0, 'full_string_intersection_sample': []}, 'var_call_TWCmnCYiL3FCciTypj0C9tpF': {'total_books_in_books_table': 200, 'total_reviews_in_review_table': 1833, 'books_with_extracted_year': 0, 'books_with_reviews_and_year': 0, 'decade_stats_all': [], 'eligible_decades': [], 'best_decade': None}}

exec(code, env_args)
