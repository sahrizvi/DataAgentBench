code = """import json
import pandas as pd

df_book_details_filtered = pd.DataFrame(json.loads(locals()['var_function-call-6896024141194000025']))
with open(locals()['var_function-call-1405526381805546238'], 'r') as f:
    review_data = json.load(f)
df_review = pd.DataFrame(review_data)

df_review['rating'] = pd.to_numeric(df_review['rating'], errors='coerce')

merged_df = pd.merge(df_book_details_filtered, df_review, left_on='book_id', right_on='purchase_id', how='inner')

decade_stats = merged_df.groupby('publication_decade').agg(
    distinct_books=('book_id', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()

filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

highest_avg_rating_decade = filtered_decades.loc[filtered_decades['average_rating'].idxmax()]

result = str(highest_avg_rating_decade['publication_decade'])

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-8650260862451553998': 'file_storage/function-call-8650260862451553998.json', 'var_function-call-6896024141194000025': [{'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'publication_year': 2014.0, 'publication_decade': 2010.0}, {'book_id': 'bookid_43', 'details': 'The book was published on September 3, 2015, and is available in English. It has a file size of 257 KB and allows unlimited simultaneous device usage. The features include Text to Speech, support for screen readers, and enhanced typesetting. However, X Ray is not enabled. Additionally, Word Wise is enabled, and sticky notes can be utilized on Kindle Scribe. The print length of the book is 31 pages.', 'publication_year': 2015.0, 'publication_decade': 2010.0}, {'book_id': 'bookid_44', 'details': 'This book was published on January 2, 2019, and is available in English. The file size is 1532 KB, and it allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is activated, and sticky notes can be used on Kindle Scribe. The print length of the book is 201 pages.', 'publication_year': 2019.0, 'publication_decade': 2010.0}, {'book_id': 'bookid_47', 'details': 'The book was published on January 1, 1986, by an unspecified publisher and is written in English.', 'publication_year': 1986.0, 'publication_decade': 1980.0}, {'book_id': 'bookid_76', 'details': 'The book was published on December 8, 2013, and is available in English. It has a file size of 1671 KB and allows for unlimited simultaneous device usage. The text-to-speech feature is enabled, and it supports screen readers. Enhanced typesetting is also enabled, although X-Ray and Word Wise features are not available. Readers can make sticky notes using Kindle Scribe, and the print length of the book is 24 pages.', 'publication_year': 2013.0, 'publication_decade': 2010.0}, {'book_id': 'bookid_107', 'details': 'This book was independently published on March 17, 2022, and is written in English. It comprises 447 pages and has an ISBN 13 of 979-8546882006. The item weighs 1.66 pounds and measures 6 x 1.12 x 9 inches.', 'publication_year': 2022.0, 'publication_decade': 2020.0}, {'book_id': 'bookid_130', 'details': 'The Fun Gang Book, published in its first edition on June 25, 2020, is available in English and features a print length of 32 pages. The file size of the book is 96,259 KB, and it allows for unlimited simultaneous device usage. However, it does not have Text to Speech, enhanced typesetting, X-Ray, Word Wise, or sticky notes enabled.', 'publication_year': 2020.0, 'publication_decade': 2020.0}, {'book_id': 'bookid_136', 'details': 'The book "Cooking for the Rushed; Revised and Updated Edition," published on December 1, 2010, is available in English and features a paperback format consisting of 192 pages. It has an ISBN-10 of 0968522637 and an ISBN-13 of 978-0968522639. The item weighs 1.65 pounds and its dimensions are 5.11 x 1.11 x 8.11 inches.', 'publication_year': 2010.0, 'publication_decade': 2010.0}, {'book_id': 'bookid_200', 'details': 'This book, published in its first edition on December 1, 2000, is available in English and features a paperback format comprising 656 pages. It has an ISBN-10 of 0762707879 and an ISBN-13 of 978-0762707874. The item weighs 2.25 pounds and has dimensions of 1 x 8.5 x 10.75 inches.', 'publication_year': 2000.0, 'publication_decade': 2000.0}], 'var_function-call-1405526381805546238': 'file_storage/function-call-1405526381805546238.json'}

exec(code, env_args)
