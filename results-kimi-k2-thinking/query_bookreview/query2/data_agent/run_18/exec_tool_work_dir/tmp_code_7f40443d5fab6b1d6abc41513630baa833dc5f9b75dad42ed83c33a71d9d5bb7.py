code = """# Check what's in the sample data
sample_result = locals()['var_functions.query_db:5']
import json
print('__RESULT__:')
print(json.dumps(str(sample_result)[:500]))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
