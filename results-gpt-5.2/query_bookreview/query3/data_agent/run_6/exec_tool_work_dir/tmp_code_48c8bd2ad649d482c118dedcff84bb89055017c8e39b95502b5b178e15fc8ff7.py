code = """import json, pandas as pd, ast

def load_tool_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

rows = load_tool_result(var_call_yapuexyAJOuQsxgrMyvnMufZ)
df = pd.DataFrame(rows)

def author_name(a):
    if a is None:
        return None
    s = str(a)
    if s.strip() in ['None','nan','NaN','']:
        return None
    if s.strip().startswith('{'):
        try:
            d = json.loads(s)
            if isinstance(d, dict):
                return d.get('name')
        except Exception:
            try:
                d = ast.literal_eval(s)
                if isinstance(d, dict):
                    return d.get('name')
            except Exception:
                return s
    return s

df['author_name'] = df['author'].apply(author_name)
df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce')
df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
df = df.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

def sanitize_title(t):
    if t is None:
        return ''
    return str(t).replace('\n',' ').replace('\r',' ').strip()

lines = []
for _, r in df.iterrows():
    author = r['author_name'] if isinstance(r['author_name'], str) and r['author_name'].strip() else 'Unknown'
    title = sanitize_title(r['title'])
    line = f"{title} — {author} — avg rating {float(r['avg_rating']):.2f} (n={int(r['review_count'])})"
    lines.append(line)

answer = "\n".join(lines)
print('__RESULT__:')
print(json.dumps(answer))"""

env_args = {'var_call_DXQVgeruDohRbsUQ7y5jaZc3': 'file_storage/call_DXQVgeruDohRbsUQ7y5jaZc3.json', 'var_call_KyuZbjj3gUVjJO1ppLTevWkF': 'file_storage/call_KyuZbjj3gUVjJO1ppLTevWkF.json', 'var_call_yapuexyAJOuQsxgrMyvnMufZ': 'file_storage/call_yapuexyAJOuQsxgrMyvnMufZ.json'}

exec(code, env_args)
