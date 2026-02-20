code = """import json

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v,'r',encoding='utf-8') as f:
            return json.load(f)
    return v

recs = load(var_call_uDSbWfRezFTQdeTB3ERdEGrB)
lines = []
for r in recs:
    title = r.get('title')
    avg = float(r.get('avg_rating'))
    cnt = int(r.get('review_count'))
    lines.append('- {} — avg rating {:.2f} (from {} reviews since 2020)'.format(title, avg, cnt))

header = 'Books in Children\'s Books with average rating >= 4.5 from 2020+ reviews:'
answer = header + "\n" + "\n".join(lines)
print('__RESULT__:')
print(json.dumps(answer, ensure_ascii=False))"""

env_args = {'var_call_JyYgk4vt6lsd5zXM4bjvPjYU': 'file_storage/call_JyYgk4vt6lsd5zXM4bjvPjYU.json', 'var_call_G8lt0q73Fq5vRRIBHFCIer5a': 'file_storage/call_G8lt0q73Fq5vRRIBHFCIer5a.json', 'var_call_uDSbWfRezFTQdeTB3ERdEGrB': 'file_storage/call_uDSbWfRezFTQdeTB3ERdEGrB.json'}

exec(code, env_args)
