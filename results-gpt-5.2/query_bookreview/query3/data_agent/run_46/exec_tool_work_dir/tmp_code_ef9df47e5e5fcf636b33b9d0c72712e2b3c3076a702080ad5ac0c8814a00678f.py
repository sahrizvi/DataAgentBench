code = """import json, pandas as pd

src = var_call_KhRIWguuXpxjhvZXJEPvJHlp
if isinstance(src, str):
    with open(src, 'r', encoding='utf-8') as f:
        recs = json.load(f)
else:
    recs = src

df = pd.DataFrame(recs)

def author_name(a):
    if a is None:
        return None
    if isinstance(a, dict):
        return a.get('name')
    if isinstance(a, str):
        s = a.strip()
        if s.startswith('{') and '"name"' in s:
            try:
                j = json.loads(s)
                if isinstance(j, dict) and 'name' in j:
                    return j.get('name')
            except Exception:
                pass
        return s
    return str(a)

if not df.empty:
    df['author'] = df['author'].apply(author_name)
    df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce').round(2)
    df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce').astype('Int64')
    df = df.sort_values(['avg_rating','review_count','title'], ascending=[False,False,True])

# keep relevant columns
out = df[['title','author','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_DCq3Dq04KeSS7Vvwy43FuJcF': 'file_storage/call_DCq3Dq04KeSS7Vvwy43FuJcF.json', 'var_call_8Q0EnG1k1bAgn81yXla1UUb7': 'file_storage/call_8Q0EnG1k1bAgn81yXla1UUb7.json', 'var_call_KhRIWguuXpxjhvZXJEPvJHlp': 'file_storage/call_KhRIWguuXpxjhvZXJEPvJHlp.json'}

exec(code, env_args)
