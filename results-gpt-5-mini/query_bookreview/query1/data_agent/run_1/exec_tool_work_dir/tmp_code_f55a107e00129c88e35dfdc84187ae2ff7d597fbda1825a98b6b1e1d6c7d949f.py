code = """import json, re
books_path = var_call_mgh9ob5dcKUeDO89uHrr4IUc
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

out = []
for b in books[:100]:
    details = b.get('details')
    if not isinstance(details, str):
        years = []
    else:
        years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", details)
    out.append({'book_id': b.get('book_id'), 'details_preview': (details[:200] if isinstance(details,str) else None), 'years_found': years})

print('__RESULT__:')
import json
print(json.dumps(out))"""

env_args = {'var_call_olewwEUuShxXJ2uEYtMawO89': ['books_info'], 'var_call_ZzgS1iTAYTwhiKjy61oq2Gth': ['review'], 'var_call_mgh9ob5dcKUeDO89uHrr4IUc': 'file_storage/call_mgh9ob5dcKUeDO89uHrr4IUc.json', 'var_call_8c7MOoJAmwZLvXCKT3ZbfT1q': 'file_storage/call_8c7MOoJAmwZLvXCKT3ZbfT1q.json', 'var_call_jeKqTvUuTNXBzAEGT5b0ML0R': None, 'var_call_ZYxxwl4ZTj5qv08wj86TlRqN': {'total_books_in_books_table': 200, 'distinct_books_with_reviews': 200, 'books_with_extracted_year': 0, 'decade_stats_all': [], 'top_decades_by_avg_rating': [], 'sample_merged_rows': []}, 'var_call_Dnw1YOiED7zod6bPJ9AOFOVX': 'file_storage/call_Dnw1YOiED7zod6bPJ9AOFOVX.json'}

exec(code, env_args)
