code = """import json
import re

output = []

try:
    with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
        books_data = json.load(f)
    output.append(f"Num books: {len(books_data)}")
    
    if books_data:
        output.append(f"First book keys: {list(books_data[0].keys())}")
        output.append(f"First book ID: {books_data[0].get('book_id')}")
        output.append(f"First book details: {books_data[0].get('details')[:50]}...")
        
        # Test regex
        bid = books_data[0].get('book_id')
        m = re.search(r'bookid_(\d+)', str(bid))
        if m:
            output.append(f"Regex match: {m.group(1)}")
        else:
            output.append("Regex no match")
            
        details = books_data[0].get('details')
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', str(details))
        output.append(f"Years found: {years}")

except Exception as e:
    output.append(f"Error: {e}")

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json', 'var_function-call-1497323203245629920': 'Done', 'var_function-call-11749323720662552993': 'None', 'var_function-call-11496871228647915128': 'Done'}

exec(code, env_args)
