code = """import json, pandas as pd

def load_json_if_path(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

rows = load_json_if_path(var_call_7aJIOWqPxFovByGFI0LRhy7J)
df = pd.DataFrame(rows)

# parse author name if JSON-like

def parse_author(a):
    if a is None:
        return None
    if isinstance(a, str):
        s = a.strip()
        if s == '' or s.lower() == 'none':
            return None
        if s.startswith('{') and '"name"' in s:
            try:
                obj = json.loads(s)
                if isinstance(obj, dict) and 'name' in obj:
                    return obj['name']
            except Exception:
                return a
    return a

if not df.empty:
    df['author'] = df['author'].apply(parse_author)
    df['avg_rating'] = df['avg_rating'].astype(float).round(2)

out = df.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])
out = out[['title','author','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_vy07jqTpl3MmEDqGJyw5pS5D': 'file_storage/call_vy07jqTpl3MmEDqGJyw5pS5D.json', 'var_call_6TCS7s6GHWTwiAhzqTdc3Bpo': 'file_storage/call_6TCS7s6GHWTwiAhzqTdc3Bpo.json', 'var_call_7aJIOWqPxFovByGFI0LRhy7J': 'file_storage/call_7aJIOWqPxFovByGFI0LRhy7J.json'}

exec(code, env_args)
