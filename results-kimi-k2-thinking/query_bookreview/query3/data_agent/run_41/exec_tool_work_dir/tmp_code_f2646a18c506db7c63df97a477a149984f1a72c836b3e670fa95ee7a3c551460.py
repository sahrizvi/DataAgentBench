code = """import json, os

# Check available variables
storage_vars = [k for k in locals().keys() if k.startswith('var_')]
print('__RESULT__:')
print(json.dumps(storage_vars))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': []}

exec(code, env_args)
