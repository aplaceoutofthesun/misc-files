#!/usr/bin/env python3
#
"""Simple script to make a new notepad file with header."""
import os

from argparse import ArgumentParser

SAVEDIR = os.path.join(os.getenv('USERPROFILE'), "Documents")

def main(filename=None):
    "Does the magic."

    top = "=" * 80 + "\n"
    mid = "*" + (" " * 78) + "*\n"
    bottom = top + "\n\n"
    temp_text = "*" + (" " * 30) + "INSERT TITLE HERE" + (" " * 30) + " *\n"
    head = top + mid + mid + temp_text + mid + mid + bottom

    if filename is None:
        filename = 'NEW_text_file.txt'
    if '.' in filename or ',' in filename and not filename.endswith('.txt'):
        filename = filename.replace('.', '-').replace(',', '-')
        filename = filename.replace('-txt', '')
    if not filename.endswith('.txt'):
        filename += ".txt"

    savepath = os.path.join(SAVEDIR, filename)

    with open(savepath, 'w', encoding='utf-8') as txt:
        txt.write(head)


if __name__ == "__main__":
    # pass

    PARSER = ArgumentParser()
    PARSER.add_argument('-f', '--filename', action='store')

    main(filename=PARSER.parse_args().filename)
