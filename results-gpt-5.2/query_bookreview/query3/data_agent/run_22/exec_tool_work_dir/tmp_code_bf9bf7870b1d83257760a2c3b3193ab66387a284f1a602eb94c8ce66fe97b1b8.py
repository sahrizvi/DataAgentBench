code = """import json, pandas as pd

def load(var):
    if isinstance(var, str) and var.endswith('.json'):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

res = load(var_call_fx13K9wZsBxZDeQZayXK1K5T)
df = pd.DataFrame(res)

def clean_author(a):
    if a is None:
        return None
    s = str(a)
    if s == 'None':
        return None
    if s.strip().startswith('{') and '"name"' in s:
        try:
            obj = json.loads(s)
            return obj.get('name')
        except Exception:
            return s
    return s

df['author'] = df['author'].map(clean_author)

out_lines = []
for _, r in df.iterrows():
    title = r.get('title')
    author = r.get('author')
    avg_rating = float(r.get('avg_rating'))
    n_reviews = int(r.get('n_reviews'))
    if author:
        out_lines.append(f"{title} — {author} (avg rating {avg_rating:.2f} from {n_reviews} reviews since 2020)")
    else:
        out_lines.append(f"{title} (avg rating {avg_rating:.2f} from {n_reviews} reviews since 2020)")

answer = "\n".join(out_lines) if out_lines else "No Children's Books found with average rating >= 4.5 based on reviews from 2020 onwards."
print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_rQv5nHdsVH9XVmiPwBNUuncV': 'file_storage/call_rQv5nHdsVH9XVmiPwBNUuncV.json', 'var_call_BuIHgCvU7z8TT9rRLs5ITn1f': 'file_storage/call_BuIHgCvU7z8TT9rRLs5ITn1f.json', 'var_call_fx13K9wZsBxZDeQZayXK1K5T': 'file_storage/call_fx13K9wZsBxZDeQZayXK1K5T.json'}

exec(code, env_args)
