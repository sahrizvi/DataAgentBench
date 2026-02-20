code = """import json
with open(var_call_onTXloM0JQ8THyzHEIvSCvyL, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_i2r86ES2VKbfFW4QYqXV4VIQ, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

book_ids = [b.get('book_id') for b in books]
purchase_ids = [r.get('purchase_id') for r in reviews]

# Get first 50
sample = {
    'sample_book_ids': book_ids[:50],
    'sample_purchase_ids': purchase_ids[:50],
    'unique_bookid_suffixes_sample': [],
    'unique_purchaseid_suffixes_sample': []
}

import re
suf = re.compile(r'(\d+)$')
for b in book_ids[:200]:
    if isinstance(b,str):
        m = suf.search(b)
        if m:
            sample['unique_bookid_suffixes_sample'].append(m.group(1))
for p in purchase_ids[:200]:
    if isinstance(p,str):
        m = suf.search(p)
        if m:
            sample['unique_purchaseid_suffixes_sample'].append(m.group(1))

sample['unique_bookid_suffixes_sample'] = sample['unique_bookid_suffixes_sample'][:50]
sample['unique_purchaseid_suffixes_sample'] = sample['unique_purchaseid_suffixes_sample'][:50]

import json
print('__RESULT__:')
print(json.dumps(sample))"""

env_args = {'var_call_Ds69D7v9q73Ptqi0dt7mcxZm': ['books_info'], 'var_call_mhV3EIUYKkPOMykxiM8Sqmxy': ['review'], 'var_call_onTXloM0JQ8THyzHEIvSCvyL': 'file_storage/call_onTXloM0JQ8THyzHEIvSCvyL.json', 'var_call_i2r86ES2VKbfFW4QYqXV4VIQ': 'file_storage/call_i2r86ES2VKbfFW4QYqXV4VIQ.json', 'var_call_hHtpWtPGGuocyqzRrCDtmytq': {'decade': None, 'average_rating': None, 'book_count': 0}}

exec(code, env_args)
