code = """import json, re

def load(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x,'r',encoding='utf-8') as f:
            return json.load(f)
    return x

rows = load(var_call_L0mV4mufD5WgJGdl659DtgQS)

def author_name(a):
    if a is None:
        return None
    if isinstance(a, str):
        s=a.strip()
        if s in ('None',''):
            return None
        if s.startswith('{'):
            try:
                d=json.loads(s)
                return d.get('name')
            except Exception:
                return a
    return str(a)

for r in rows:
    r['author'] = author_name(r.get('author'))
    r['avg_rating'] = round(float(r['avg_rating']), 3)

answer_lines = []
for r in rows:
    t=r.get('title')
    a=r.get('author') or 'Unknown'
    avg=r.get('avg_rating')
    n=r.get('review_count')
    answer_lines.append(f"{t} — {a} (avg rating {avg} from {n} review(s) since 2020)")

final = "\n".join(answer_lines) if answer_lines else "No 'Children's Books' found with average rating >= 4.5 based on reviews from 2020 onwards."
print('__RESULT__:')
print(json.dumps(final, ensure_ascii=False))"""

env_args = {'var_call_evUY0EGx7A3iGYZkDSjP2UCX': 'file_storage/call_evUY0EGx7A3iGYZkDSjP2UCX.json', 'var_call_Xda1sPRbicIRqmuft0SvOpV9': 'file_storage/call_Xda1sPRbicIRqmuft0SvOpV9.json', 'var_call_L0mV4mufD5WgJGdl659DtgQS': 'file_storage/call_L0mV4mufD5WgJGdl659DtgQS.json'}

exec(code, env_args)
