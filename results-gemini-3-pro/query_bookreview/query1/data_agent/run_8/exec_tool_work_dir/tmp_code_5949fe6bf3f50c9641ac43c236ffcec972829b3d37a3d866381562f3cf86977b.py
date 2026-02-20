code = """import json
import re

output = []

try:
    with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
        books_data = json.load(f)
        
    b = books_data[0]
    details = b.get('details', '')
    output.append(f"Full details: {details}")
    
    # Try multiple regexes
    r1 = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    output.append(f"Regex 1 result: {r1}")
    
    r2 = re.findall(r'(\d{4})', details)
    output.append(f"Regex 2 result: {r2}")
    
    subtitle = b.get('subtitle', '')
    output.append(f"Subtitle: {subtitle}")
    r3 = re.findall(r'(\d{4})', subtitle)
    output.append(f"Subtitle regex: {r3}")

except Exception as e:
    output.append(f"Error: {e}")

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json', 'var_function-call-1497323203245629920': 'Done', 'var_function-call-11749323720662552993': 'None', 'var_function-call-11496871228647915128': 'Done', 'var_function-call-4914481013675661386': ['Num books: 200', "First book keys: ['book_id', 'details', 'subtitle']", 'First book ID: bookid_1', 'First book details: Published by Chatto & Windus, the first edition of...', 'Regex match: 1', 'Years found: []']}

exec(code, env_args)
