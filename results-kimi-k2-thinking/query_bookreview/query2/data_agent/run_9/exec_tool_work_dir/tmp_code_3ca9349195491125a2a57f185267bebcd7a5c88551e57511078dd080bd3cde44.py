code = """# Let's check the type and structure of the stored result
result = var_functions.query_db:5
print(f"Type of stored result: {type(result)}")
print(f"First 500 characters: {str(result)[:500]}")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
