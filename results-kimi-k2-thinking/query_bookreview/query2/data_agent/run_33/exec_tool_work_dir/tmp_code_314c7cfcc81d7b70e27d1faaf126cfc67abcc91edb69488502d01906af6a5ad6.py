code = """# Check what's in the storage variables
import json

# These are the keys from the tool results
keys_to_check = ['var_functions.query_db:10', 'var_functions.query_db:2', 'var_functions.query_db:12', 'var_functions.query_db:6']

for key in keys_to_check:
    if key in locals():
        print(f"{key}: {locals()[key][:200] if isinstance(locals()[key], str) else str(locals()[key])[:200]}")
    else:
        print(f"{key}: NOT FOUND")

print('__RESULT__:')
print(json.dumps({'status': 'checked'}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.query_db:8': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '2'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json'}

exec(code, env_args)
