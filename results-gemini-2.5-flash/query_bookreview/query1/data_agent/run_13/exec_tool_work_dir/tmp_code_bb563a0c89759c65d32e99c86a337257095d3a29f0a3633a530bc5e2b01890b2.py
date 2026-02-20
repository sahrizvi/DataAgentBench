code = """import pandas as pd
import json

with open(locals()['var_function-call-8221080890098848692'], 'r') as f:
    books_info = json.load(f)

df_books = pd.DataFrame(books_info)

def extract_year(details_string):
    if isinstance(details_string, str):
        import re
        match = re.search(r'published (?:by [^,]+, )?(?:in its \w+ edition )?(?:on )?((?:January|February|March|April|May|June|July|August|September|October|November|December)?(?: \d{1,2},)? )?(\d{4})', details_string)
        if match:
            return int(match.group(2))
    return None

df_books['publication_year'] = df_books['details'].apply(extract_year)
df_books['decade'] = (df_books['publication_year'] // 10) * 10

result = df_books[['book_id', 'decade']].to_json(orient='records')
print('__RESULT__:')
print(result)"""

env_args = {'var_function-call-8221080890098848692': 'file_storage/function-call-8221080890098848692.json'}

exec(code, env_args)
