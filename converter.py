import re
import mammoth
from atom_weight import atom_weight

forbidden_words = ['Макс.', 'Среднее', 'Станд. отклонение', 'стат.', 'отклонение', 'Станд.', 'Мин.']
forbidden_values = [ 'Да', 'Итог', '100.00', 'В стат.']
tables = []
converted_values = []

with open("174.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value # The generated HTML
    messages = result.messages # Any messages, such as warnings during conversion


def extract_tables(row_html):
    tables_list = re.findall(r'<table>((.|\n)*?)<\/table>', row_html)
    return tables_list


def extract_rows(row_table):
    return re.findall(r'<tr>((.|\n)*?)<\/tr>', row_table)


def clean_tags(row_html):
    return re.split('<.*?>', row_html)


def split_table_rows(table):
    return re.findall(r'<tr>((.|\n)*?)<\/tr>', table)


def clean_row(row):
    new_row = []
    for item in row:
        if not item in forbidden_words:
            new_row.append(item)
    return new_row


def remove_spaces(row):
    new_row = []
    for item in row:
        if item != '':
            new_row.append(item)
    return new_row


def remove_forbidden_values(row):
    new_row = []
    for item in row:
        if not item in forbidden_values:
            new_row.append(item)
    return new_row


html_tuple = extract_tables(html)


for table in html_tuple:
    tables.append([])
    for row in extract_rows(table[0]):
        cleaned_row = clean_tags(row[0])
        cleaned_row = remove_spaces(cleaned_row)
        if cleaned_row != [] and cleaned_row[0] not in forbidden_words:
            cleaned_row = remove_forbidden_values(cleaned_row)
            tables[-1].append(cleaned_row)


def convert_weighted_to_atomic(table):
    return [print(a) for a in zip(*table)]

#
for table in tables:
    convert_weighted_to_atomic(table)
