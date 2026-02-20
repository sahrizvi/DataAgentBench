code = """import json
import pandas as pd
import re

# First, determine what variables are available
print('__RESULT__:')
print(json.dumps({
    "available_vars": list(locals().keys())[:20],
    "var_types": {str(k): str(type(v)) for k, v in list(locals().items())[:5]}
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:3': 'file_storage/functions.query_db:3.json'}

exec(code, env_args)
