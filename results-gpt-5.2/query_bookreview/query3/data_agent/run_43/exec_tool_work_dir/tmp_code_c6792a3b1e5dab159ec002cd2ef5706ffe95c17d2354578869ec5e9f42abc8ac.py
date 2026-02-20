code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v,'r',encoding='utf-8') as f:
            return json.load(f)
    return v

rows = load(var_call_whX2RhYod7zBmv2XdtZDwEXD)
df = pd.DataFrame(rows)

# simplify author to name if JSON-like
import ast

def author_name(a):
    if a is None:
        return None
    s = str(a)
    if s in ('None','nan'):
        return None
    if s.strip().startswith('{'):
        try:
            d = json.loads(s)
            return d.get('name')
        except Exception:
            pass
    return s

df['author'] = df['author'].apply(author_name)

df = df.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

# format plain text lines
lines = []
for _, r in df.iterrows():
    lines.append(f"{r['title']} — {r['author'] or 'Unknown'} (avg rating {r['avg_rating']:.2f}, {int(r['review_count'])} reviews since 2020)")

ans = "\n".join(lines) if lines else "No Children's Books found with average rating >= 4.5 based on reviews from 2020 onwards."

print('__RESULT__:')
print(json.dumps(ans))"""

env_args = {'var_call_RjpT8Z1zunfb9lBKDcdZ28cl': 'file_storage/call_RjpT8Z1zunfb9lBKDcdZ28cl.json', 'var_call_QFhkcVDqicay7U1fezZPe7P4': 'file_storage/call_QFhkcVDqicay7U1fezZPe7P4.json', 'var_call_whX2RhYod7zBmv2XdtZDwEXD': 'file_storage/call_whX2RhYod7zBmv2XdtZDwEXD.json'}

exec(code, env_args)
