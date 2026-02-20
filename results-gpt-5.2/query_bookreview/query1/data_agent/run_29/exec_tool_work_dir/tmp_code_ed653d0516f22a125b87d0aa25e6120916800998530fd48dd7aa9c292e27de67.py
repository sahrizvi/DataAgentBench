code = """import json, re, pandas as pd

books = pd.DataFrame(var_call_6tPuPplVTDGl4T2nBzjCI05r)

# load reviews (may be file path)
rev_raw = var_call_jZXZSkmEEmrnnxaCBAPoAtt8
if isinstance(rev_raw, str) and rev_raw.endswith('.json'):
    with open(rev_raw, 'r', encoding='utf-8') as f:
        reviews_list = json.load(f)
else:
    reviews_list = rev_raw
reviews = pd.DataFrame(reviews_list)

# parse year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

books['year'] = books['details'].map(extract_year)
books = books.dropna(subset=['year']).copy()
books['year'] = books['year'].astype(int)
books['decade_start'] = (books['year']//10)*10
books['decade'] = books['decade_start'].astype(str) + 's'

# fuzzy join ids by extracting numeric suffix
num_pat = re.compile(r'(\d+)')

def id_num(x):
    if not isinstance(x, str):
        return None
    m = num_pat.search(x)
    return int(m.group(1)) if m else None

books['idnum'] = books['book_id'].map(id_num)
reviews['idnum'] = reviews['purchase_id'].map(id_num)

# ratings to float
reviews['rating'] = pd.to_numeric(reviews['rating'], errors='coerce')
reviews = reviews.dropna(subset=['rating','idnum'])
books = books.dropna(subset=['idnum'])

merged = reviews.merge(books[['idnum','decade']], on='idnum', how='inner')

# distinct books rated per decade
books_per_decade = merged.groupby('decade')['idnum'].nunique().rename('distinct_books')
avg_rating = merged.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating], axis=1).reset_index()
summary = summary[summary['distinct_books']>=10]
summary = summary.sort_values(['avg_rating','distinct_books'], ascending=[False, False])

best = summary.iloc[0]['decade'] if len(summary) else None

print('__RESULT__:')
print(json.dumps({'best_decade': best}))"""

env_args = {'var_call_6tPuPplVTDGl4T2nBzjCI05r': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_15', 'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is 0710306911, while the ISBN-13 is 978-0710306913. The item weighs 2.23 pounds and has dimensions of 5.5 x 1.25 x 8.5 inches.'}, {'book_id': 'bookid_16', 'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ISBN-10 for this book is 0130840963, while the ISBN-13 is 978-0130840967. The item weighs 1.3 pounds and has dimensions of 7.01 x 0.67 x 9.17 inches.'}, {'book_id': 'bookid_26', 'details': 'Published by Heinemann, the first edition of this book was released on March 20, 1995. Written in English, it is a paperback edition consisting of 269 pages. The book carries the ISBN 10 number 0435088432 and the ISBN 13 number 978-0435088439. It is suitable for readers aged 11 to 16 years. The item weighs 14.2 ounces and has dimensions of 6 x 0.59 x 9 inches.'}, {'book_id': 'bookid_42', 'details': 'This book, published by Belknap Press, an imprint of Harvard University Press, was released on February 19, 2018. It is written in English and is available in hardcover, consisting of 240 pages. The book has an ISBN-10 number of 0674975812 and an ISBN-13 number of 978-0674975811. It weighs 1.23 pounds and its dimensions are 6.5 x 0.75 x 9.75 inches.'}, {'book_id': 'bookid_47', 'details': 'The book was published on January 1, 1986, by an unspecified publisher and is written in English.'}, {'book_id': 'bookid_53', 'details': 'This book, published by Frank Amato Publications on January 1, 1997, is written in English and features a spiral binding with a total of 31 pages. It has an ISBN-10 number of 1571880879 and an ISBN-13 number of 978-1571880871. The item weighs 3.2 ounces and has dimensions of 5.5 x 0.25 x 8.75 inches.'}, {'book_id': 'bookid_54', 'details': 'This book, published by Dover Publications on August 1, 2006, is written in English and is suitable for readers aged 8 to 9 years. It has an ISBN-10 of 0486457117 and an ISBN-13 of 978-0486457116. The book weighs 1.01 pounds and has dimensions of 5.25 x 1.5 x 8.5 inches.'}, {'book_id': 'bookid_61', 'details': 'Published by Schiffer Pub Ltd, this UK edition was released on January 1, 1997. The book is written in English and is available in paperback, consisting of 160 pages. It has an ISBN-10 of 0887408400 and an ISBN-13 of 978-0887408403. Weighing 2 pounds, the book has dimensions of 8.5 x 0.5 x 11 inches.'}, {'book_id': 'bookid_65', 'details': 'This book, published by Putnam Pub Group, is a first edition released on February 1, 1979. It is written in English and has an ISBN-10 of 0825639255 and an ISBN-13 of 978-0825639258. The item weighs 9.6 ounces.'}, {'book_id': 'bookid_81', 'details': 'The book, published by Shoe Publishing and Street Talk Media, is a first edition released on September 16, 2014. It is written in English and consists of 162 pages in hardcover format. The ISBN-10 of the book is 0990617211, while the ISBN-13 is 978-0990617211. The item weighs 14.7 ounces.'}, {'book_id': 'bookid_86', 'details': 'The book, published by William Stout Publishers in its first edition on January 1, 2007, is available in English and features a hardcover format with a total of 262 pages. It has an ISBN-10 of 0974621439 and an ISBN-13 of 978-0974621432. The item weighs 5.35 pounds.'}, {'book_id': 'bookid_87', 'details': 'This book is published by W W Norton & Co Inc and is a first edition released on January 1, 1987. It is written in English and is available in paperback format, consisting of 279 pages. The ISBN for this book is 0393304388 for the 10-digit version and 978-0393304381 for the 13-digit version. The item weighs 11.2 ounces and has dimensions of 5.75 by 0.75 by 9 inches.'}, {'book_id': 'bookid_95', 'details': 'This book is published by Tyndale House Publishers in its 14th printing edition, released on January 1, 1985. It is written in English and comes in a paperback format, comprising 240 pages. The book has an ISBN-10 of 084236661X and an ISBN-13 of 978-0842366618. Weighing 10.4 ounces, its dimensions are 5.5 inches in width, 0.75 inches in thickness, and 8.5 inches in height.'}, {'book_id': 'bookid_127', 'details': 'This book is published by Bonanza Books in a reprint edition dated January 1, 1930. It is written in English and is available in hardcover with a total of 204 pages. The ISBN-10 for the book is 0517202484, while its ISBN-13 is 978-0517202487. The item weighs 1.95 pounds.'}, {'book_id': 'bookid_123', 'details': 'The book, published by Aspen Publishers on July 27, 2010, is written in English and is available in paperback format, comprising 1,232 pages. It has an ISBN-10 number of 0735590591 and an ISBN-13 number of 978-0735590595. The item weighs 3.1 pounds and has dimensions of 7 x 1.25 x 10 inches.'}, {'book_id': 'bookid_134', 'details': 'Published by Champagne Books, the first edition of this book was released on August 6, 2015. It is written in English and spans 250 pages in paperback format. The book has an ISBN-10 of 1771552026 and an ISBN-13 of 978-1771552028. It weighs 10.4 ounces and has dimensions of 5.5 x 0.57 x 8.5 inches.'}, {'book_id': 'bookid_136', 'details': 'The book "Cooking for the Rushed; Revised and Updated Edition," published on December 1, 2010, is available in English and features a paperback format consisting of 192 pages. It has an ISBN-10 of 0968522637 and an ISBN-13 of 978-0968522639. The item weighs 1.65 pounds and its dimensions are 5.11 x 1.11 x 8.11 inches.'}, {'book_id': 'bookid_144', 'details': 'The book is published by Baen in a reissue edition dated September 25, 2018. It is written in English and is available as a mass market paperback, consisting of 528 pages. The ISBN-10 for this edition is 1481483536, while the ISBN-13 is 978-1481483537. The item weighs 8.8 ounces and has dimensions of 4.13 x 1.3 x 6.75 inches.'}, {'book_id': 'bookid_149', 'details': 'This book is independently published and was released on November 13, 2021. It is written in English and consists of 95 pages in paperback format. The ISBN-13 for this title is 979-8480568868, and it has a weight of 4.2 ounces. The dimensions of the book are 5 x 0.22 x 8 inches.'}, {'book_id': 'bookid_160', 'details': 'This book, published by Scala Publishers on July 12, 2006, is available in English and spans 112 pages. It has an ISBN-10 of 1857592379 and an ISBN-13 of 978-1857592375. The item weighs 1.05 pounds and its dimensions are 8.74 x 0.41 x 8.68 inches.'}, {'book_id': 'bookid_168', 'details': 'The book, published by Harcourt School Publishers in its first edition on January 1, 2008, is available in English and consists of 179 pages. It has an ISBN-10 of 015343631X and an ISBN-13 of 978-0153436314. The item weighs 13.5 ounces.'}, {'book_id': 'bookid_192', 'details': "This book, published by Chicago's Books Press, is a first edition released on July 21, 2008. It is written in English and has a total of 200 pages in paperback format. The ISBN-10 for this edition is 0979789214, while the ISBN-13 is 978-0979789212. The item weighs 1.7 pounds."}, {'book_id': 'bookid_199', 'details': 'The book, published by Editorial de Ciencia Sociales, is a first edition released on January 1, 2004. It is written in Spanish and is available in paperback, encompassing a total of 378 pages.'}], 'var_call_jZXZSkmEEmrnnxaCBAPoAtt8': 'file_storage/call_jZXZSkmEEmrnnxaCBAPoAtt8.json'}

exec(code, env_args)
