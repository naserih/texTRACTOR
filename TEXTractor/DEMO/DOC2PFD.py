#DOC2PFD.py
import sys
import os
# import comtypes.client
import win32com.client

wdFormatPDF = 17

doc_database = './data/.doc/'
pdf_database = './data/pdf/'
in_files = [f for f in os.listdir(doc_database) if "$" not in f]

word = win32com.client.Dispatch('Word.Application')
for in_file in in_files:
    in_file_name = doc_database+in_file
    out_file_name = pdf_database+in_file+'.pdf'
    in_file = os.path.abspath(in_file_name)
    out_file = os.path.abspath(out_file_name)
    print (in_file)
    print (out_file)
    # word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
doc.Close()
word.Quit()