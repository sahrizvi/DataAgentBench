code = """import json
import pandas as pd
import ast
import os

# Check what variable names are available
available_vars = [k for k in locals().keys() if k.startswith('var_')]
print('Available variables:', available_vars)

# For now, let's check if the files exist with different patterns
result_files = []
for root, dirs, files in os.walk('/tmp'):
    for file in files:
        if file.endswith('.json'):
            result_files.append(os.path.join(root, file))

print('JSON files found:', result_files)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': []}

exec(code, env_args)
