code = """print("__RESULT__:")
result = var_functions.query_db:4
print(type(result))
print(str(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json'}

exec(code, env_args)
