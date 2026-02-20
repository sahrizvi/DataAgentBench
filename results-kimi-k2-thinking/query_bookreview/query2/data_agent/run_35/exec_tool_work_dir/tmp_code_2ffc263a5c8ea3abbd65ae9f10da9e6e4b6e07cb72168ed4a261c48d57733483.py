code = """# Check the type and structure of the books data
data = locals()['var_functions.query_db:2']
print('Type of data:', type(data))
print('Data:', data)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review']}

exec(code, env_args)
