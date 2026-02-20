code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v,'r',encoding='utf-8') as f:
            return json.load(f)
    return v

res = load(var_call_EhCJ3DfjBvd7YtNj2jBSBSmQ)
df = pd.DataFrame(res)

# simplify author to name when possible

def author_name(a):
    if a is None or (isinstance(a,float) and pd.isna(a)):
        return None
    s = str(a)
    try:
        obj = json.loads(s)
        if isinstance(obj, dict) and 'name' in obj:
            return obj.get('name')
    except Exception:
        pass
    return s

df['author'] = df['author'].map(author_name)

df = df.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

lines = []
for _, r in df.iterrows():
    lines.append(f"{r['title']} — {'' if r['author'] in [None,'None'] else r['author']} (avg rating {r['avg_rating']:.2f}, {int(r['review_count'])} reviews since 2020)")

answer = "\n".join(lines)
print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_xq7UQLxFmadi7LYXNyevVkyU': 'file_storage/call_xq7UQLxFmadi7LYXNyevVkyU.json', 'var_call_mFlN8wd6p9q5kAQbhHOu8kYp': 'file_storage/call_mFlN8wd6p9q5kAQbhHOu8kYp.json', 'var_call_EhCJ3DfjBvd7YtNj2jBSBSmQ': 'file_storage/call_EhCJ3DfjBvd7YtNj2jBSBSmQ.json'}

exec(code, env_args)
