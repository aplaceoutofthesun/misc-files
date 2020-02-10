#!/usr/bin/env python
#
# bookjoin.py - small script to join a folder of pdf files into a single file

import os
import sys
import shutil

import PyPDF2

def main(target_path, output_fname=None):

    if not os.path.exists(target_path) or not os.path.isdir(target_path):
        sys.exit("Check the target path.\nIt must be an existing directory.\n")

    files_to_merge = [x for x in os.listdir(target_path) if x.endswith(".pdf")]

    print("The following files will be merged:")
    for f in files_to_merge:
        print(" - {} ".format(f))

    if input("\nContinue? ").lower() == 'n':
        sys.exit(1)

    
    merger = PyPDF2.PdfFileMerger()
    reader = PyPDF2.PdfFileReader
    
    
    if output_fname is None:
        out = os.path.abspath(target_path).split('\\')
        output_fname = ''.join([out, "_merged.pdf"])

    for target_file in files_to_merge:
        try:
            target_file = os.path.join(target_path, target_file)
            
            pdf_obj = open(target_file, 'rb')
            pdf_file = reader(pdf_obj)
            merger.append(pdf_file)
            
            pdf_obj.close()
        except IOError as io_err:
            print("IOError: {}".format(io_err))
            print("** STACK **\n{}".format(sys.exc_info()[0]))

    merger.write(output_fname)
    merger.close()

if __name__ == "__main__":
    # print(len(sys.argv), sys.argv)
    # sys.exit()
    
    if len(sys.argv) <= 1:
        sys.exit("Insufficient args.")
    if len(sys.argv) == 2:
        main(sys.argv[1])
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])