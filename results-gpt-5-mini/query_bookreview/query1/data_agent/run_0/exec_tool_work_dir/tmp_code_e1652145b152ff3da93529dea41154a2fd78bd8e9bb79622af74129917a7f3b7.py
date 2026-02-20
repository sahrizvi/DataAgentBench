code = """import json, re
import pandas as pd

with open(var_call_nIZtqYm1WnlSxW3jofWcK6ID, 'r') as f:
    books = json.load(f)
with open(var_call_yhdg6aG3UawDmz5sv6LZzVf5, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# normalize reviews rating
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# normalize ids
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# function to extract year with heuristics
def extract_year_heuristic(detail):
    if not isinstance(detail, str):
        return None
    # try to find 'published' and search nearby for 4-digit
    low = detail.lower()
    idx = low.find('published')
    if idx != -1:
        window = detail[max(0, idx-30): idx+80]
        m = re.search(r"(1[5-9][0-9]{2}|20[0-2][0-9]|2023|\d{4})", window)
        if m:
            try:
                y=int(m.group(0))
                if 1500<=y<=2023:
                    return y
            except:
                pass
    # fallback: find all 4-digit sequences anywhere
    all4 = re.findall(r"\d{4}", detail)
    for s in all4:
        try:
            y=int(s)
            if 1500<=y<=2023:
                return y
        except:
            continue
    return None

# apply
if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year_heuristic)
else:
    df_books['pub_year'] = None

# compute per-book mean rating
book_mean = df_reviews.groupby('book_id', dropna=True)['rating'].mean().reset_index().rename(columns={'rating':'mean_rating'})

# merge with books
merged = pd.merge(book_mean, df_books[['book_id','pub_year']], on='book_id', how='left')

# count stats
total_books = len(df_books)
books_with_pubyear = int(df_books['pub_year'].notna().sum())
matched_with_pubyear = int(merged['pub_year'].notna().sum())

# filter to those with pub_year
merged_valid = merged[merged['pub_year'].notna()].copy()
if not merged_valid.empty:
    merged_valid['pub_year'] = merged_valid['pub_year'].astype(int)
    merged_valid['decade'] = merged_valid['pub_year'].apply(lambda y: f"{(y//10)*10}s")
    decade_grp = merged_valid.groupby('decade').agg(book_count=('book_id','nunique'), avg_book_rating=('mean_rating','mean')).reset_index()
    decade_filtered = decade_grp[decade_grp['book_count']>=10].copy()
    if not decade_filtered.empty:
        decade_filtered = decade_filtered.sort_values(['avg_book_rating','book_count'], ascending=[False, False])
        best = decade_filtered.iloc[0]
        result = {'decade': best['decade'], 'avg_rating': round(float(best['avg_book_rating']),4), 'book_count': int(best['book_count'])}
    else:
        result = {'decade': None, 'avg_rating': None, 'book_count': 0}
else:
    decade_grp = pd.DataFrame(columns=['decade','book_count','avg_book_rating'])
    result = {'decade': None, 'avg_rating': None, 'book_count': 0}

out = {
    'result': result,
    'total_books': int(total_books),
    'books_with_pubyear': int(books_with_pubyear),
    'matched_with_pubyear': int(matched_with_pubyear),
    'decade_groups': decade_grp.sort_values('decade').to_dict(orient='records')
}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_WjxSnom9ZZcw1f2zfM8y68hn': ['books_info'], 'var_call_Qgq3KUZEryaZofz9J0cBHUJB': ['review'], 'var_call_NVoEnkMvFVyDYFIhkNKQFyML': 'file_storage/call_NVoEnkMvFVyDYFIhkNKQFyML.json', 'var_call_yhdg6aG3UawDmz5sv6LZzVf5': 'file_storage/call_yhdg6aG3UawDmz5sv6LZzVf5.json', 'var_call_UIXpxuBL5mV0zLs0iHxlnjQu': {'decade': None, 'avg_rating': None, 'book_count': 0}, 'var_call_nIZtqYm1WnlSxW3jofWcK6ID': 'file_storage/call_nIZtqYm1WnlSxW3jofWcK6ID.json', 'var_call_2Ajd2K3gfeO0QAv9ozU1eszn': {'decade': None, 'avg_rating': None, 'book_count': 0}, 'var_call_7T44ie4sxpubTLaTSjdzX47g': {'total_reviews': 1833, 'unique_review_books': 200, 'total_books': 200, 'books_with_pubyear': 0, 'unique_books_with_rating': 200, 'matched_with_pubyear': 0, 'decades': []}, 'var_call_W2y5B6cpa6osqRAnSnK9elR5': {'num_books': 200, 'samples': [{'book_id': 'bookid_1', 'details_sample': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of', 'matches': []}, {'book_id': 'bookid_2', 'details_sample': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN', 'matches': []}, {'book_id': 'bookid_3', 'details_sample': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363', 'matches': []}, {'book_id': 'bookid_4', 'details_sample': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575', 'matches': []}, {'book_id': 'bookid_5', 'details_sample': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it s', 'matches': []}, {'book_id': 'bookid_6', 'details_sample': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0', 'matches': []}, {'book_id': 'bookid_7', 'details_sample': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.', 'matches': []}, {'book_id': 'bookid_8', 'details_sample': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-di', 'matches': []}, {'book_id': 'bookid_9', 'details_sample': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-16946217', 'matches': []}, {'book_id': 'bookid_10', 'details_sample': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 o', 'matches': []}, {'book_id': 'bookid_11', 'details_sample': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-0893011673. Weighing 1.51 pounds, the book me', 'matches': []}, {'book_id': 'bookid_12', 'details_sample': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978', 'matches': []}, {'book_id': 'bookid_13', 'details_sample': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN', 'matches': []}, {'book_id': 'bookid_14', 'details_sample': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 of 1087848539 and an ISBN-13 of 978-10878', 'matches': []}, {'book_id': 'bookid_15', 'details_sample': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is ', 'matches': []}, {'book_id': 'bookid_16', 'details_sample': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ', 'matches': []}, {'book_id': 'bookid_17', 'details_sample': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477110190 and an ISBN-13 number of 978-8477', 'matches': []}, {'book_id': 'bookid_18', 'details_sample': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an ISBN-10 of 1275627234 and an ISBN-13 of 97', 'matches': []}, {'book_id': 'bookid_19', 'details_sample': 'The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 1609303687 and an ISBN-13 number of 978-160930', 'matches': []}, {'book_id': 'bookid_20', 'details_sample': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of 2295 KB and supports various features s', 'matches': []}]}, 'var_call_JEu1JZGFvj5jyNKsmOwJxtuT': [{'index': 0, 'book_id': 'bookid_1', 'contains_2004': True, 'details_start': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English a'}, {'index': 1, 'book_id': 'bookid_2', 'contains_2004': False, 'details_start': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperb'}, {'index': 2, 'book_id': 'bookid_3', 'contains_2004': False, 'details_start': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bo'}, {'index': 3, 'book_id': 'bookid_4', 'contains_2004': False, 'details_start': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consis'}, {'index': 4, 'book_id': 'bookid_5', 'contains_2004': False, 'details_start': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimi'}, {'index': 5, 'book_id': 'bookid_6', 'contains_2004': False, 'details_start': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN '}, {'index': 6, 'book_id': 'bookid_7', 'contains_2004': True, 'details_start': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January '}, {'index': 7, 'book_id': 'bookid_8', 'contains_2004': False, 'details_start': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and sp'}, {'index': 8, 'book_id': 'bookid_9', 'contains_2004': False, 'details_start': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in '}, {'index': 9, 'book_id': 'bookid_10', 'contains_2004': True, 'details_start': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprise'}], 'var_call_74bKUsxLVyQ5saHKwAFvbbqF': {'result': {'decade': None, 'avg_rating': None, 'book_count': 0}, 'decades_all': [], 'total_books_with_year': 0, 'unique_review_books': 200}, 'var_call_TE09J5WJCENMGaSuaPqYCwan': {'count_with_year': 0, 'samples': [{'book_id': 'bookid_1', 'matches': [], 'pub_year': None, 'details_start': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English a'}, {'book_id': 'bookid_2', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperb'}, {'book_id': 'bookid_3', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bo'}, {'book_id': 'bookid_4', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consis'}, {'book_id': 'bookid_5', 'matches': [], 'pub_year': None, 'details_start': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimi'}, {'book_id': 'bookid_6', 'matches': [], 'pub_year': None, 'details_start': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN '}, {'book_id': 'bookid_7', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January '}, {'book_id': 'bookid_8', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and sp'}, {'book_id': 'bookid_9', 'matches': [], 'pub_year': None, 'details_start': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in '}, {'book_id': 'bookid_10', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprise'}, {'book_id': 'bookid_11', 'matches': [], 'pub_year': None, 'details_start': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 o'}, {'book_id': 'bookid_12', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprisin'}, {'book_id': 'bookid_13', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback for'}, {'book_id': 'bookid_14', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format '}, {'book_id': 'bookid_15', 'matches': [], 'pub_year': None, 'details_start': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and i'}, {'book_id': 'bookid_16', 'matches': [], 'pub_year': None, 'details_start': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is'}, {'book_id': 'bookid_17', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44'}, {'book_id': 'bookid_18', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback f'}, {'book_id': 'bookid_19', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 p'}, {'book_id': 'bookid_20', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print le'}, {'book_id': 'bookid_21', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Random House in its first edition on January 1, 1945, is written in English and weighs 12 ounces.'}, {'book_id': 'bookid_22', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by KCTS Television on March 6, 2006, is written in English and features a spiral-bound format with '}, {'book_id': 'bookid_23', 'matches': [], 'pub_year': None, 'details_start': 'This book, published independently on July 1, 2021, is written in English and is available in paperback with a total of '}, {'book_id': 'bookid_24', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Little Brown in its first edition on January 1, 1939, is available in English. It has an ISBN-10'}, {'book_id': 'bookid_25', 'matches': [], 'pub_year': None, 'details_start': 'This book is written in English and is available in a paperback format consisting of 8 pages. It has an ISBN 10 number o'}, {'book_id': 'bookid_32', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Mantra Lingua / Tsai Fong on January 1, 1998, is available in both English and Arabic. It has an'}, {'book_id': 'bookid_26', 'matches': [], 'pub_year': None, 'details_start': 'Published by Heinemann, the first edition of this book was released on March 20, 1995. Written in English, it is a paper'}, {'book_id': 'bookid_27', 'matches': [], 'pub_year': None, 'details_start': 'This book is written in English and has an ISBN-10 of 0553819399 and an ISBN-13 of 978-0553819397. It weighs 1.06 pounds'}, {'book_id': 'bookid_28', 'matches': [], 'pub_year': None, 'details_start': 'This book, published by Thames and Hudson Ltd on March 20, 1995, is available in English. It has an ISBN-10 of 050001655'}, {'book_id': 'bookid_29', 'matches': [], 'pub_year': None, 'details_start': 'The book, published by Brookside Press in a supplement edition on November 10, 2017, is written in English and spans 264'}]}}

exec(code, env_args)
