import re
import mammoth
from atom_weight import atom_weight
from bs4 import BeautifulSoup

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


def add_zero_value(row):
    # print(row)
    new_row = ""
    soup = BeautifulSoup(row, 'html.parser')
    tags = soup.find_all("td")
    for tag in tags:
        tag = str(tag)
        if tag == "<td></td>":
            tag = "<td>0</td>"
            new_row += tag
        else:
            new_row += tag
    return new_row


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


def remove_emtpy_row(row):
    if row[0] == '0':
        return
    return row


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
        string_without_spaces = add_zero_value(row[0])
        cleaned_row = clean_tags(string_without_spaces)
        cleaned_row = remove_spaces(cleaned_row)
        cleaned_row = remove_emtpy_row(cleaned_row)
        if cleaned_row != None and cleaned_row[0] not in forbidden_words:
            cleaned_row = remove_forbidden_values(cleaned_row)
            tables[-1].append(cleaned_row)

# def zip_by_element(table):
#     return [a for a in zip(*table)]


spectrus = []
atomic_weight = []


for table in tables:
    new_table = []
    new_table.append(table[0])
    table_length = len(table)

    for cycle in range(table_length):
        new_table.append([])

    current_position = 1
    current_table = 1

    for element in table[0][1:]:
        for atomic in atom_weight:
            if element == atomic[0]:
                while current_position < table_length:
                    new_table[current_position].append(float(table[current_table][current_position])/atomic[1])
                    current_position += 1

    print(new_table)

#
# def convert_to_atomic(spectre):
#     title = spectre[0]
#     atomic_weight[-1].append(title)
#     temp = []
#     for row in spectre[1:]:
#         # print(row)
#         for item in atom_weight:
#             if row[0] == item[0]:
#                 temp.append(item[0])
#                 for element in row[1:]:
#                     temp.append(float(element))
#         atomic_weight[-1].append(tuple(temp))
#         temp = []
#
#
# for spectre in spectrus:
#     atomic_weight.append([])
#     convert_to_atomic(spectre)


# print(atomic_weight)
