code = """import json
import pandas as pd
import re

# Read the books data with English and Literature & Fiction filter
with open('/tmp/tmp1i2h0y6b.json', 'r') as f:
    books_data = json.load(f)

# Read the reviews data
with open('/tmp/tmpq8g8s3q7.json', 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Convert rating to float
reviews_df['rating'] = reviews_df['rating'].astype(float)

# Display data info for debugging
result = {"books_shape": books_df.shape, "reviews_shape": reviews_df.shape}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.query_db:8': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '2'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json'}

exec(code, env_args)
