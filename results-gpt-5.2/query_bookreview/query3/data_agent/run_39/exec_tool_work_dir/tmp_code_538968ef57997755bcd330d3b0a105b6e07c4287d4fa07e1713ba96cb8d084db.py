code = """import json

def load(obj):
    if isinstance(obj, str) and obj.endswith('.json'):
        with open(obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return obj

rows = load(var_call_7FFPseQqh0r6zSVBuNI2BwbF)

def author_name(a):
    if a is None:
        return None
    s = str(a).strip()
    if s.startswith('{'):
        try:
            j = json.loads(s)
            if isinstance(j, dict) and 'name' in j:
                return j.get('name')
        except Exception:
            return str(a)
    return str(a)

out_lines = []
for r in rows:
    out_lines.append({
        'title': r.get('title'),
        'author': author_name(r.get('author')),
        'avg_rating_2020_onwards': r.get('avg_rating'),
        'review_count_2020_onwards': r.get('review_count')
    })

header = "Books in 'Children\'s Books' with avg rating >= 4.5 (reviews from 2020+):\n"
lines = []
for r in out_lines:
    title = r['title']
    author = r['author'] or 'Unknown'
    avg = r['avg_rating_2020_onwards']
    cnt = r['review_count_2020_onwards']
    lines.append(f"- {title} — {author} (avg {avg}, n={cnt})")
text = header + "\n".join(lines) + "\n"

print('__RESULT__:')
print(json.dumps(text, ensure_ascii=False))"""

env_args = {'var_call_qa3W5cMz8ihg1yvYmD3kiRP1': 'file_storage/call_qa3W5cMz8ihg1yvYmD3kiRP1.json', 'var_call_khHHf4pVkHSTyF1IQTdKf1Nb': 'file_storage/call_khHHf4pVkHSTyF1IQTdKf1Nb.json', 'var_call_7FFPseQqh0r6zSVBuNI2BwbF': 'file_storage/call_7FFPseQqh0r6zSVBuNI2BwbF.json'}

exec(code, env_args)
