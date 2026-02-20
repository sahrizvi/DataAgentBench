code = """import json
books_path = var_call_mgh9ob5dcKUeDO89uHrr4IUc
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
# collect first 30 book_id and details
out = []
for i, b in enumerate(books[:30]):
    out.append({'idx': i, 'book_id': b.get('book_id'), 'details': b.get('details')})
print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_olewwEUuShxXJ2uEYtMawO89': ['books_info'], 'var_call_ZzgS1iTAYTwhiKjy61oq2Gth': ['review'], 'var_call_mgh9ob5dcKUeDO89uHrr4IUc': 'file_storage/call_mgh9ob5dcKUeDO89uHrr4IUc.json', 'var_call_8c7MOoJAmwZLvXCKT3ZbfT1q': 'file_storage/call_8c7MOoJAmwZLvXCKT3ZbfT1q.json', 'var_call_jeKqTvUuTNXBzAEGT5b0ML0R': None, 'var_call_ZYxxwl4ZTj5qv08wj86TlRqN': {'total_books_in_books_table': 200, 'distinct_books_with_reviews': 200, 'books_with_extracted_year': 0, 'decade_stats_all': [], 'top_decades_by_avg_rating': [], 'sample_merged_rows': []}}

exec(code, env_args)
