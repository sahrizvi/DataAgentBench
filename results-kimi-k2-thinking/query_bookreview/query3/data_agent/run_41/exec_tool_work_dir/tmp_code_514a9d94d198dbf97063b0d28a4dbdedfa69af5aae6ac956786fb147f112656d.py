code = """import json, os

# Check what's in storage
print("Storage keys:", [k for k in locals().keys() if k.startswith('var_')])

# Try to access the result
result_keys = [k for k in locals().keys() if 'functions.query_db' in k]
if result_keys:
    key = result_keys[0]
    print(f"Found result key: {key}")
    data = locals()[key]
    print(f"Data type: {type(data)}")
    if isinstance(data, str) and os.path.exists(data):
        print(f"Loading from file: {data}")
        with open(data, 'r') as f:
            data = json.load(f)
        print(f"Number of records: {len(data)}")
        if len(data) > 0:
            print("First record:", data[0])
    else:
        print("Data is not a file path or doesn't exist")
        if isinstance(data, list):
            print(f"Number of records: {len(data)}")
            if len(data) > 0:
                print("First record:", data[0])
        else:
            print("Data value:", data)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': []}

exec(code, env_args)
