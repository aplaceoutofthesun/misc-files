#!/usr/bin/env python3
#
"""Uses some code from A. Parrish's 'Letters as Numbers' work to build and
return a searchable index of Unicode characters, plus their metadata.

* Unicode Data (Current version: 12.1.0):
  https://www.unicode.org/Public/12.1.0/ucd/UnicodeData.txt

"""
# import sys
# import random
import logging

from argparse import ArgumentParser

LOG_CONF = "[+] %(asctime)s-%(levelname)s-%(message)s [%(lineno)d]"
logging.basicConfig(format=LOG_CONF, level=logging.INFO)

def build_index():
    "Builds a searchable index from the Unicode Database."
    ucode = []

    with open('UnicodeData.txt', 'r', encoding='ascii') as db_file:
        ucode_file = db_file.read().split('\n')
        for line in ucode_file:
            line = line.strip()
            fields = line.split(';')
            row = {
                'char': chr(int(fields[0], 16)),
                'name': fields[1],
                'category': fields[2]
            }
            ucode.append(row)
    return ucode

def search_index(ucode_index, search_terms, with_char):

    logging.info("Char present: %s", with_char)

    logging.info("Building Index...")
    ucode = build_index()
    logging.info("Index Built.")

    # ucode_index
    # print(type(ucode), ucode[:10])
    # if not with_char:
    #     print('hello')

    found = []

    logging.info("Beginning search...")

    if not with_char:
        logging.info("withchar FALSE.")
        logging.info("Term: %s, Index: %s.", search_terms, ucode_index)
        # if ucode_index == 'name':
        for term in search_terms:
            for row in ucode:
                if term.upper() in row[ucode_index]:
                    found.append(row)
    if with_char:

        logging.info("withchar TRUE.")
        logging.info("Term: %s, Index: %s", search_terms, ucode_index)
        # if ucode_index == 'category':
        for term in search_terms:
            for row in ucode:
                if term.upper() in row[ucode_index]:
                    found.append(row['char'])
                    # pass
    logging.info("%d", len(found))
    # cats = [row['char'] for row in ucode if 'CAT ' in row['name']]

    # print(found)
    for i in found:
        print(i, end="; ")



def shit():
    # # Now, 'ucode' holds a list of dictionaries that can be search with a
    # # conditional expression:
    # roman = [row for row in ucode if 'ROMAN NUMERAL' in row['name']]
    # for i in roman:
    #     pass
    #     # print(i)

    # # A version with cats using the 'char' key in the predicate position of the
    # # list expression, returning just matching chars:
    # # NB: Must use 'CAT ' with the space otherwise other chars are found...
    # cats = [row['char'] for row in ucode if 'CAT ' in row['name']]
    # for i in cats:
    #     print(i, end=', ')

    # # A cat composition:
    # for i in range(10):
    #     print(''.join(random.sample(cats, len(cats))))

    # # Mathematical arrows:
    # arrows = [row['char'] for row in ucode
    #           if 'ARROW' in row['name']
    #           and row['category'] == 'Sm']

    # print(arrows)

    # # An arrow composition:
    # arrow_comp = ''.join([random.choice(arrows) for i in range(1500)])
    # print(arrow_comp)

    # # CHAOS!!!
    # non_control_chars = [row['char'] for row in ucode
    #                      if row['category'][0] != 'C']
    # # print(non_control_chars) # DO NOT DO THIS! TOO BIG!
    # print(''.join([random.choice(non_control_chars) for i in range(500)]))
    pass

def main():
    parser = ArgumentParser()

    valid_keys = 'Keys: category, name, char'

    parser.add_argument('ucode_index',
                        action='store',
                        default='name',
                        help='The key to use to search the Database'\
                                ' (default: %(default)s) '\
                                    f'{valid_keys}')

    parser.add_argument('search_terms',
                        nargs='+',
                        action='store',
                        help='The term(s) to search for in the Database')

    parser.add_argument('-wc', '--withchar',
                        action='store_true',
                        default=False,
                        help='Use "char" in the predicate position of the' \
                         ' search string.')

    args = parser.parse_args()

    ucode_index = args.ucode_index
    search_terms = args.search_terms
    with_char = args.withchar

    search_index(ucode_index, search_terms, with_char)


if __name__ == "__main__":
    main()
