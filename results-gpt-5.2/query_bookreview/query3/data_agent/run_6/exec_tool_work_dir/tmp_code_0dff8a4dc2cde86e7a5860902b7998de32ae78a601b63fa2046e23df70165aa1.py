code = """import json

def load_tool_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

rows = load_tool_result(var_call_yapuexyAJOuQsxgrMyvnMufZ)
# return raw rows as pretty text
lines = []
for r in rows:
    lines.append("{title} | avg_rating={avg_rating} | n={review_count}".format(**r))
answer = "\n".join(lines)
print('__RESULT__:')
print(json.dumps(answer))"""

env_args = {'var_call_DXQVgeruDohRbsUQ7y5jaZc3': 'file_storage/call_DXQVgeruDohRbsUQ7y5jaZc3.json', 'var_call_KyuZbjj3gUVjJO1ppLTevWkF': 'file_storage/call_KyuZbjj3gUVjJO1ppLTevWkF.json', 'var_call_yapuexyAJOuQsxgrMyvnMufZ': 'file_storage/call_yapuexyAJOuQsxgrMyvnMufZ.json'}

exec(code, env_args)
