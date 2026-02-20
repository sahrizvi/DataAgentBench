code = """import json
import pandas as pd

books_details_path = locals()['var_function-call-15840768285559180515']
with open(books_details_path, 'r') as f:
    books_details = json.load(f)

df_books = pd.DataFrame(books_details)

def extract_year(details):
    import re
    match = re.search(r'published (?:by [^,]+, )?(?:in its \w+ edition )?on (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, (\d{4})|published (?:by [^,]+, )?(?:in its \w+ edition )?in (?:January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})|published (?:by [^,]+, )?on (\d{4})'', details)
    if match:
        if match.group(1):
            return int(match.group(1))
        elif match.group(2):
            return int(match.group(2))
        elif match.group(3):
            return int(match.group(3))
    match_year_only = re.search(r'edition on \w+ \d+, (\d{4})|published (?:by [^,]+, )?in (\d{4})|published (?:on )?(\d{4})', details)
    if match_year_only:
        if match_year_only.group(1):
            return int(match_year_only.group(1))
        elif match_year_only.group(2):
            return int(match_year_only.group(2))
        elif match_year_only.group(3):
            return int(match_year_only.group(3))
    return None

df_books['publication_year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['publication_year'])
df_books['publication_decade'] = (df_books['publication_year'] // 10 * 10).astype(int)

result = df_books[['book_id', 'publication_decade']].to_json(orient='records')
print('__RESULT__:')
print(result)"""

env_args = {'var_function-call-2890100811406089170': ['books_info'], 'var_function-call-15840768285559180515': 'file_storage/function-call-15840768285559180515.json'}

exec(code, env_args)
