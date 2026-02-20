code = """import json, pandas as pd

def load(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

recs = load(var_call_J9sznd3QW0GAgYm3KSc8qoFc)
df = pd.DataFrame(recs)

# simplify author to name if JSON-like
import ast

def author_name(x):
    if x is None:
        return None
    if isinstance(x, str):
        s = x.strip()
        if s.startswith('{') and s.endswith('}'):
            try:
                d = json.loads(s)
                return d.get('name')
            except Exception:
                try:
                    d = ast.literal_eval(s)
                    if isinstance(d, dict):
                        return d.get('name')
                except Exception:
                    return x
        return x
    return str(x)

df['author'] = df['author'].apply(author_name)

# Build plain text lines
lines = []
for _, r in df.iterrows():
    lines.append(f"{r['title']} — {r['author'] if pd.notna(r['author']) else 'Unknown'} (avg rating {float(r['avg_rating']):.2f}, {int(r['review_count'])} reviews since 2020)")

answer = "\n".join(lines) if lines else "No Children's Books found with average rating ≥ 4.5 based on reviews from 2020 onwards."
print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_7Pd9ZRzPSleASAQEENVZonsG': 'file_storage/call_7Pd9ZRzPSleASAQEENVZonsG.json', 'var_call_HB5MBFbyCpynho7sEuw6VLyx': 'file_storage/call_HB5MBFbyCpynho7sEuw6VLyx.json', 'var_call_J9sznd3QW0GAgYm3KSc8qoFc': 'file_storage/call_J9sznd3QW0GAgYm3KSc8qoFc.json'}

exec(code, env_args)
