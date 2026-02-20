code = """import json, pandas as pd

src = var_call_pDTDUlpArUEW8UWkBpA9JH7M
if isinstance(src, str):
    with open(src, 'r', encoding='utf-8') as f:
        recs = json.load(f)
else:
    recs = src

df = pd.DataFrame(recs)
out = df[['title','avg_rating','review_count']].to_dict(orient='records')

lines = []
for r in out:
    title = str(r['title'])
    avg = float(r['avg_rating'])
    n = int(r['review_count'])
    lines.append(f"- {title} — avg rating {avg:.2f} (n={n} reviews since 2020)")

answer = "Books in 'Children's Books' with average rating >= 4.5 from 2020 onwards:" + "\n" + "\n".join(lines)

print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_EdAWrgeosZLhYPf9vtDUS5T8': 'file_storage/call_EdAWrgeosZLhYPf9vtDUS5T8.json', 'var_call_SU1DIgG6u7rTQRZomNngXmwS': 'file_storage/call_SU1DIgG6u7rTQRZomNngXmwS.json', 'var_call_pDTDUlpArUEW8UWkBpA9JH7M': 'file_storage/call_pDTDUlpArUEW8UWkBpA9JH7M.json'}

exec(code, env_args)
