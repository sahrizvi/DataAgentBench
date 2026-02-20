code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

rows = load(var_call_9vcCboTmdcElr1cBhviKEWDv)
df = pd.DataFrame(rows)

# simplify author to name if it's a json string

def author_name(a):
    if a is None:
        return None
    s = str(a)
    if s == 'None':
        return None
    s_strip = s.strip()
    if s_strip.startswith('{') and s_strip.endswith('}'):
        try:
            j = json.loads(s_strip)
            if isinstance(j, dict) and 'name' in j:
                return j['name']
        except Exception:
            return s
    return s

if not df.empty:
    df['author'] = df['author'].apply(author_name)
    df['avg_rating'] = df['avg_rating'].round(2)
    df = df.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = df.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_ygnxXSPAGS5GH9gBsYhssmcx': 'file_storage/call_ygnxXSPAGS5GH9gBsYhssmcx.json', 'var_call_EarXTGzKkZ9KIEMXcrpXjZTM': 'file_storage/call_EarXTGzKkZ9KIEMXcrpXjZTM.json', 'var_call_9vcCboTmdcElr1cBhviKEWDv': 'file_storage/call_9vcCboTmdcElr1cBhviKEWDv.json'}

exec(code, env_args)
