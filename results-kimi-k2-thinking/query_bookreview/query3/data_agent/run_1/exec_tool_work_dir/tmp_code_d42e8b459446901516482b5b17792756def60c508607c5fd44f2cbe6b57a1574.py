code = """import os
import glob

# List all files in /tmp directory to find the actual files
tmp_files = glob.glob('/tmp/*')
print("Files in /tmp:", tmp_files)

# Find json files
json_files = [f for f in tmp_files if f.endswith('.json')]
print("JSON files:", json_files)

# Also check if we have variables defined
globals_dict = globals()
locals_dict = locals()

# List any variable that might contain file paths
for key in globals_dict:
    if 'query_db' in str(key):
        print(f"Variable {key}:", globals_dict[key])
        
for key in locals_dict:
    if 'query_db' in str(key):
        print(f"Variable {key}:", locals_dict[key])"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json'}

exec(code, env_args)
