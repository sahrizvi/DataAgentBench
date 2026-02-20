code = """import json, pandas as pd

src = var_call_i1u9loDbObTGtYG6B2nIgSUi
if isinstance(src, str):
    with open(src, 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    data = src

df = pd.DataFrame(data)

df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce')
df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')

def clean_author(a):
    if a is None:
        return None
    if isinstance(a, str):
        s=a.strip()
        if s.lower()=='none' or s=='':
            return None
        if s.startswith('{'):
            try:
                j=json.loads(s)
                if isinstance(j, dict) and 'name' in j:
                    return j['name']
            except Exception:
                pass
        return s
    return str(a)

df['author_clean'] = df['author'].apply(clean_author)

out_df = df[['title','author_clean','avg_rating','review_count']].rename(columns={'author_clean':'author'})
out_df = out_df.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = out_df.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_kF382lWp3SOh2h05IBnnvzZ5': 'file_storage/call_kF382lWp3SOh2h05IBnnvzZ5.json', 'var_call_606cSpwU57bNWSqXO9YkOaoc': 'file_storage/call_606cSpwU57bNWSqXO9YkOaoc.json', 'var_call_i1u9loDbObTGtYG6B2nIgSUi': 'file_storage/call_i1u9loDbObTGtYG6B2nIgSUi.json'}

exec(code, env_args)
