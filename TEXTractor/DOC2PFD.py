#DOC2PFD.py
import sys
import os


SOURCE = 'SERVER'
database = 'TS_MET_notes'
doc_database = '../data/notes/'+database
pdf_database = '../data/pdfs/'+database+'/ALL/'
patient_data = {}
if SOURCE == 'SERVER':
    patient_folders = [str(f) for f in os.listdir(doc_database)]
    for folder in patient_folders:
        patient_data[folder] = [f for f in os.listdir('%s/%s'%(doc_database,folder)) if 'ConsultNote' in f]
    print(patient_data)
    for patient in patient_data:
        for note in patient_data[patient]:
            patient_file_path = '%s/%a/%s'%(doc_database,patient,note)
            pdf_out_path = '%s/%a_%s.pdf'%(pdf_database,patient,note)
            print(pdf_out_path)
            os.system("abiword --to=pdf -o %s %s"%(pdf_out_path, patient_file_path))
    # os.system("abiword --to=pdf -o static/data/notes/pdf/3.pdf static/data/notes/doc/3.doc")

elif SOURCE == 'LOCAL':
    import comtypes
    # import win32com.client
    wdFormatPDF = 17

    doc_database = './'
    pdf_database = './'
    in_files = [f for f in os.listdir(doc_database) if "$" not in f and ".doc" in f]
    print(infiles)

    word = comtypes.client.CreateObject('Word.Application')
    # word = win32com.client.Dispatch('Word.Application')
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


