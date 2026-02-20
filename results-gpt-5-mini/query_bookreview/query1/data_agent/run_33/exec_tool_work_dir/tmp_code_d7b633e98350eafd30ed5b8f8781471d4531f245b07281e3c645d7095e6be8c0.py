code = """import json
import pandas as pd
import re

with open(var_call_onTXloM0JQ8THyzHEIvSCvyL, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_i2r86ES2VKbfFW4QYqXV4VIQ, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# function to extract numeric suffix
def extract_num_id(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)$', s)
    if m:
        return m.group(1)
    m2 = re.search(r'(\d+)', s)
    return m2.group(1) if m2 else None

# more robust year extraction: find all four-digit numbers between 1500 and 2023
def extract_year(text):
    if not isinstance(text, str):
        return None
    matches = re.findall(r'(1[5-9]\d{2}|20\d{2})', text)
    if matches:
        # choose the first reasonable year within 1500-2023
        for m in matches:
            try:
                y = int(m)
                if 1500 <= y <= 2023:
                    return y
            except:
                continue
    return None

# apply
df_books['num_id'] = df_books.get('book_id').apply(extract_num_id)
df_reviews['num_id'] = df_reviews.get('purchase_id').apply(extract_num_id)
df_books['year'] = df_books.get('details').apply(extract_year)

# Convert ratings
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = None

# Drop rows lacking num_id or rating
df_reviews = df_reviews.dropna(subset=['num_id','rating'])
df_books = df_books.dropna(subset=['num_id'])

# Merge on num_id
merged = pd.merge(df_reviews, df_books, on='num_id', how='inner', suffixes=('_rev','_book'))

# Keep only merged rows where year is present
merged_year = merged[merged['year'].notna()].copy()

result = None
if merged_year.empty:
    result = {'decade': None, 'average_rating': None, 'book_count': 0}
else:
    # compute average rating per book
    book_avg = merged_year.groupby('book_id').agg({'rating':'mean','year':'first'}).reset_index()
    book_avg['year'] = book_avg['year'].astype(int)
    book_avg['decade_start'] = (book_avg['year'] // 10) * 10
    book_avg['decade'] = book_avg['decade_start'].astype(str) + 's'
    # group by decade
    dec_group = book_avg.groupby('decade').agg(book_count=('book_id','nunique'), average_rating=('rating','mean')).reset_index()
    dec_group = dec_group[dec_group['book_count'] >= 10]
    if dec_group.empty:
        result = {'decade': None, 'average_rating': None, 'book_count': 0}
    else:
        best = dec_group.sort_values(['average_rating','book_count'], ascending=[False, False]).iloc[0]
        result = {'decade': best['decade'], 'average_rating': float(round(best['average_rating'],4)), 'book_count': int(best['book_count'])}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_Ds69D7v9q73Ptqi0dt7mcxZm': ['books_info'], 'var_call_mhV3EIUYKkPOMykxiM8Sqmxy': ['review'], 'var_call_onTXloM0JQ8THyzHEIvSCvyL': 'file_storage/call_onTXloM0JQ8THyzHEIvSCvyL.json', 'var_call_i2r86ES2VKbfFW4QYqXV4VIQ': 'file_storage/call_i2r86ES2VKbfFW4QYqXV4VIQ.json', 'var_call_hHtpWtPGGuocyqzRrCDtmytq': {'decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_8qjO34eLn8UKugtVoYazAfLL': {'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20', 'bookid_21', 'bookid_22', 'bookid_23', 'bookid_24', 'bookid_25', 'bookid_32', 'bookid_26', 'bookid_27', 'bookid_28', 'bookid_29', 'bookid_30', 'bookid_31', 'bookid_33', 'bookid_34', 'bookid_35', 'bookid_36', 'bookid_37', 'bookid_38', 'bookid_56', 'bookid_39', 'bookid_40', 'bookid_41', 'bookid_42', 'bookid_43', 'bookid_62', 'bookid_44', 'bookid_45', 'bookid_46', 'bookid_47', 'bookid_48'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167', 'purchaseid_188', 'purchaseid_23', 'purchaseid_196', 'purchaseid_196', 'purchaseid_3', 'purchaseid_48', 'purchaseid_154', 'purchaseid_99', 'purchaseid_190', 'purchaseid_3', 'purchaseid_169', 'purchaseid_3', 'purchaseid_145', 'purchaseid_194', 'purchaseid_81', 'purchaseid_199', 'purchaseid_48', 'purchaseid_96', 'purchaseid_167', 'purchaseid_196', 'purchaseid_196', 'purchaseid_196', 'purchaseid_148', 'purchaseid_8', 'purchaseid_145', 'purchaseid_200', 'purchaseid_8', 'purchaseid_178', 'purchaseid_20', 'purchaseid_52', 'purchaseid_159', 'purchaseid_83', 'purchaseid_67', 'purchaseid_3', 'purchaseid_58', 'purchaseid_196', 'purchaseid_95', 'purchaseid_76', 'purchaseid_3', 'purchaseid_62'], 'unique_bookid_suffixes_sample': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '32', '26', '27', '28', '29', '30', '31', '33', '34', '35', '36', '37', '38', '56', '39', '40', '41', '42', '43', '62', '44', '45', '46', '47', '48'], 'unique_purchaseid_suffixes_sample': ['186', '191', '190', '8', '178', '186', '76', '186', '115', '167', '188', '23', '196', '196', '3', '48', '154', '99', '190', '3', '169', '3', '145', '194', '81', '199', '48', '96', '167', '196', '196', '196', '148', '8', '145', '200', '8', '178', '20', '52', '159', '83', '67', '3', '58', '196', '95', '76', '3', '62']}, 'var_call_Dd8hkFf37v8QbXlQ7FdQUZkQ': {'stats': {'num_books_total': 200, 'num_reviews_total': 1833, 'num_books_with_num_id': 200, 'num_reviews_with_num_id': 1833, 'num_books_with_year': 0, 'merged_all_count': 1833, 'merged_unique_book_ids': 200, 'merged_with_year_count': 0, 'merged_with_year_unique_books': 0}, 'sample_merged': []}, 'var_call_qCmFbT1oGdSBCVKjfhmuBTvu': 'file_storage/call_qCmFbT1oGdSBCVKjfhmuBTvu.json'}

exec(code, env_args)
