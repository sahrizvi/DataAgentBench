code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

rows = load(var_call_nwbfWNpdGTQgsIiXnP0ITweV)
df = pd.DataFrame(rows)

# clean author to name if it's a json string
import ast

def author_name(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x)
    try:
        obj = json.loads(s)
        if isinstance(obj, dict) and 'name' in obj:
            return obj.get('name')
    except Exception:
        pass
    return s

df['author'] = df['author'].apply(author_name)

# keep relevant columns
out_df = df[['title','author','avg_rating','review_count']].copy()
out_df['avg_rating'] = out_df['avg_rating'].round(3)

out = out_df.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_nC144DvUfh0RHZM2NL4RmKYn': 'file_storage/call_nC144DvUfh0RHZM2NL4RmKYn.json', 'var_call_oJXrpHmh6TDGpUTQUM87hD8P': 'file_storage/call_oJXrpHmh6TDGpUTQUM87hD8P.json', 'var_call_nwbfWNpdGTQgsIiXnP0ITweV': 'file_storage/call_nwbfWNpdGTQgsIiXnP0ITweV.json'}

exec(code, env_args)
