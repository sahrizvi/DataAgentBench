code = """import json

def load_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

rows = load_result(var_call_Tjn7sPJ3T3GCFioHXKsYd0WM)

lines = []
for r in rows:
    avg = float(r.get('avg_rating'))
    cnt = int(r.get('review_count'))
    title = str(r.get('title'))
    lines.append(f"{title} - avg rating {avg:.2f} (n={cnt})")

header = "Books in Children" + "'" + "s Books with average rating >= 4.5 from 2020+ reviews:"
answer = header + "\n" + "\n".join(lines)

print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_pq4JLdaQIQjDPq2rv1zZvyl8': 'file_storage/call_pq4JLdaQIQjDPq2rv1zZvyl8.json', 'var_call_xmOI7FuGbjSjeOuxXgyRHWzm': 'file_storage/call_xmOI7FuGbjSjeOuxXgyRHWzm.json', 'var_call_Tjn7sPJ3T3GCFioHXKsYd0WM': 'file_storage/call_Tjn7sPJ3T3GCFioHXKsYd0WM.json'}

exec(code, env_args)
