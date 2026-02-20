code = """import json

with open(var_call_Qxuw05rvUjND9SrR7ZrMoFcJ, 'r') as f:
    data = json.load(f)

output = []
for item in data:
    output.append({
        'title': item.get('title'),
        'author': item.get('author'),
        'avg_rating': item.get('avg_rating'),
        'review_count': item.get('review_count')
    })

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_0C8uwpKxowvKhWAtQ9COH81A': ['books_info'], 'var_call_SimpA06dt5RaDc35kN1qJ4Cx': 'file_storage/call_SimpA06dt5RaDc35kN1qJ4Cx.json', 'var_call_63Llc1wtT8Vnf7jIFuUKPat5': ['review'], 'var_call_wQPw2fgJXAbet4r995pYeSuD': 'file_storage/call_wQPw2fgJXAbet4r995pYeSuD.json', 'var_call_tLgGZXXhjmb6Lj8euRf6k2DA': 'file_storage/call_tLgGZXXhjmb6Lj8euRf6k2DA.json', 'var_call_Qxuw05rvUjND9SrR7ZrMoFcJ': 'file_storage/call_Qxuw05rvUjND9SrR7ZrMoFcJ.json'}

exec(code, env_args)
