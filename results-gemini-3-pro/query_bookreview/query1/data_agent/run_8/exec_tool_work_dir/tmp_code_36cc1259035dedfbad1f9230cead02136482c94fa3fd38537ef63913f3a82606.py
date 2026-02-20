code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-13869118034911199914'], 'r') as f:
    reviews_data = json.load(f)

print(f"Books data length: {len(books_data)}")
if len(books_data) > 0:
    print(f"First book: {books_data[0]}")

print(f"Reviews data length: {len(reviews_data)}")
if len(reviews_data) > 0:
    print(f"First review: {reviews_data[0]}")

# Test extraction on first item
b = books_data[0]
bid = b.get('book_id', '')
details = b.get('details', '')
print(f"Book ID: {bid}, Details: {details[:50]}...")
m = re.search(r'bookid_(\d+)', str(bid))
if m:
    print(f"Extracted Book Num: {m.group(1)}")
else:
    print("Failed to extract Book Num")

r = reviews_data[0]
pid = r.get('purchase_id', '')
rating = r.get('rating')
print(f"Purchase ID: {pid}, Rating: {rating}")
m = re.search(r'purchaseid_(\d+)', str(pid))
if m:
    print(f"Extracted Purchase Num: {m.group(1)}")
else:
    print("Failed to extract Purchase Num")

print("__RESULT__:")
print(json.dumps("Done"))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json'}

exec(code, env_args)
