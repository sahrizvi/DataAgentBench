code = """import json
import pandas as pd

with open(locals()['var_function-call-8650260862451553998'], 'r') as f:
    book_details = json.load(f)

df_book_details = pd.DataFrame(book_details)

def extract_year(details):
    import re
    match = re.search(r'published (?:by [^,]+, )?(?:in its \w+ edition )?(?:on )?((?:January|February|March|April|May|June|July|August|September|October|November|December)?(?: \d{1,2},)? (\d{4}))', details)
    if match:
        return int(match.group(2))
    return None

df_book_details['publication_year'] = df_book_details['details'].apply(extract_year)
df_book_details['publication_decade'] = (df_book_details['publication_year'] // 10) * 10

# Filter out entries where publication_decade is NaN
df_book_details_filtered = df_book_details.dropna(subset=['publication_decade'])

print("__RESULT__:")
print(df_book_details_filtered.to_json(orient='records'))"""

env_args = {'var_function-call-8650260862451553998': 'file_storage/function-call-8650260862451553998.json'}

exec(code, env_args)
