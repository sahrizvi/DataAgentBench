code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v,'r',encoding='utf-8') as f:
            return json.load(f)
    return v

rows = load(var_call_ibgloknXF0EzzUGpNYPKSN4C)
df = pd.DataFrame(rows)

def author_name(a):
    if a is None:
        return None
    if isinstance(a, str):
        s = a.strip()
        if s.lower() == 'none' or s == '':
            return None
        if s.startswith('{'):
            try:
                return json.loads(s).get('name')
            except Exception:
                return s
        return s
    return str(a)

df['author'] = df['author'].apply(author_name)

lines = []
for _, r in df.iterrows():
    title = r['title']
    author = r['author'] if (pd.notna(r['author']) and r['author']) else 'Unknown'
    avg = float(r['avg_rating_2020_onwards'])
    cnt = int(r['review_count_2020_onwards'])
    plural = 's' if cnt != 1 else ''
    line = f"{title} — {author} (avg rating since 2020: {avg:.2f} from {cnt} review{plural})"
    lines.append(line)

answer = "\\n".join(lines)
print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_gcNpdv5zgLv5oLQOs0fohwQT': 'file_storage/call_gcNpdv5zgLv5oLQOs0fohwQT.json', 'var_call_9ggSiybxgY6W7v6s2wBwP9WL': 'file_storage/call_9ggSiybxgY6W7v6s2wBwP9WL.json', 'var_call_ibgloknXF0EzzUGpNYPKSN4C': 'file_storage/call_ibgloknXF0EzzUGpNYPKSN4C.json'}

exec(code, env_args)
