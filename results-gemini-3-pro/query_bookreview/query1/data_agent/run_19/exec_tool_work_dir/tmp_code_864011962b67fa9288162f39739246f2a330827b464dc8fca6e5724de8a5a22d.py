code = """import json
import re
import pandas as pd

file_path_books = locals()['var_function-call-3096561497567485986']
with open(file_path_books, 'r') as f:
    books_data = json.load(f)

books_df = pd.DataFrame(books_data)

def extract_year(row):
    text = str(row.get('details', ''))
    # Look for 4 digits (19xx or 20xx)
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    if years:
        return int(years[-1]) # Take the last one found
    
    text_sub = str(row.get('subtitle', ''))
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text_sub)
    if years:
        return int(years[-1])
    return None

books_df['year'] = books_df.apply(extract_year, axis=1)

# Count valid years
valid_years_count = books_df['year'].notna().sum()
sample_years = books_df[['title', 'details', 'year']].head(20).to_dict(orient='records')

print("__RESULT__:")
print(json.dumps({
    "valid_years_count": int(valid_years_count),
    "sample_years": sample_years
}))"""

env_args = {'var_function-call-10944610125865916082': ['books_info'], 'var_function-call-7623816645255018684': 'file_storage/function-call-7623816645255018684.json', 'var_function-call-4621741179361575125': [{'count': '200'}], 'var_function-call-14482848130311299562': [{'COUNT(*)': '1833'}], 'var_function-call-8131521746694899491': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-3096561497567485986': 'file_storage/function-call-3096561497567485986.json', 'var_function-call-5332796046984058542': 'file_storage/function-call-5332796046984058542.json', 'var_function-call-12575391759179135184': {'error': 'No decade met the criteria.'}, 'var_function-call-15019832477204085469': {'book_ids_count': 200, 'review_ids_count': 200, 'overlap_count': 200, 'sample_overlap': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}}

exec(code, env_args)
