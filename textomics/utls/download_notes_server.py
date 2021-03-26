'''
This routine is built to download patient document from ARIA database.
ARIA databae is on mssql.
'''

import os
import pymssql
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import requests
import lxml.html as lh
from datetime import datetime
import csv
import env

load_dotenv()


MEDPHYS_API = os.getenv("MEDPHYS_API")
V_FILEDATA = os.getenv("V_FILEDATA")
DOCUMENT_PATH = os.getenv("DOCUMENT_PATH")
PATIENT_LIST_CSV = os.getenv("PATIENT_LIST_CSV")
END_OF_TREATMENT_NOTES = ['ro - end of treatment note', 'end of treatment note']
CONSULT_NOTES = ['ro - consult', 'consult']
FOLLOWUP_NOTES = ['follow up note', 'ro - follow-up note']
NURSING_NOTES = ['nursing note','ro - nursing note','intra treatment note',
                    'nursing miscellaneous','ro - nursing miscellaneous',]
UNK_NOTES = ['ro - patient document', 'ro - note','note', 'oncology note']
OTHER_NOTES = [
'appointment sheet',
'brachy dose distribution',
'brachy oncentra plan summary',
'brachy plato plan summary',
'brachy worksheet',
'brachytherapy note',
'brachytherapy prescription',
'brachytherapy requisition',
'brachytherapy treatment record',
'brachytherapy treatment sheet',
'consent',
'coordination and patient liaison note',
'ct contrast',
'ct medtec breast board',
'ct planning sheet',
'cytology report',
'daily clarity alignment',
'distribution',
'dqa results',
'eclipse distribution',
'eclipse dvh',
'eclipse imrt',
'eclipse isocenter shift',
'eclipse step and shoot',
'electron planning requisition',
'electron tx setup sheet',
'hematology',
'hematology pre-oacis',
'hematology tests',
'hematology tests pre-oacis',
'insurance disability forms',
'miscellaneous',
'nut - consult note',
'nut - follow-up note',
'nutrionist follow up',
'nutrition consult',
'operative report',
'outside pathology',
'outside radiology',
'pathology',
'patient management images',
'patient setup images',
'planning note',
'pmr note',
'prescriptions',
'prostate - tumor registry pro code',
'rad onc requistion',
'radcalc',
'radiology pre-oacis',
'radiology report',
'radiology requisition',
'radiotherapy prescription',
'req-ecg',
'req-labs',
'req-labs stat',
'req-medical consultation',
'req-medical consultation emergency room',
'req-mri consent english',
'req-palliative care',
'req-pet scan',
'req-pharmacy fax prescription',
'req-psychosocial oncology referral',
'req-pulmonary function',
'req-radiology/nuclear medicine',
'request for consult',
'return appointment form',
'ro - addendum',
'ro - brachy dose distribution',
'ro - brachy oncentra plan summary',
'ro - brachy worksheet',
'ro - brachytherapy note',
'ro - brachytherapy prescription',
'ro - brachytherapy treatment record',
'ro - checklist',
'ro - ck distribution',
'ro - ck pathlist',
'ro - ck plan report',
'ro - ct brainlab setup',
'ro - ct contrast',
'ro - ct medtech breastboard',
'ro - ct planning sheet',
'ro - eclipse distribution',
'ro - eclipse dvh',
'ro - eclipse imrt',
'ro - eclipse report',
'ro - electron planning requisition',
'ro - follow-up ent rvh',
'ro - incident report',
'ro - insurance disability forms',
'ro - intra treatment note',
'ro - manual calc photon',
'ro - mri sim contrast media',
'ro - nursing assessment flowsheet',
'ro - pacemaker form',
'ro - pacemaker scan',
'ro - patient management images',
'ro - patient setup images',
'ro - peer review note',
'ro - plan sum',
'ro - planning note',
'ro - pmr note',
'ro - protocol note',
'ro - protocol note screen failure',
'ro - rad onc requisition',
'ro - radcalc',
'ro - radiotherapy prescription',
'ro - replan request',
'ro - request for consult',
'ro - rtt worksheet',
'ro - scanned rad onc dictations',
'ro - scanned rad onc requisition',
'ro - sim/ct sim setup',
'ro - simple plan evaluation',
'ro - site group review note - ent',
'ro - stereo distribution',
'ro - treatment info outside',
'ro - treatment prescription',
'rtt worksheet',
'scanned rad onc dictations',
'sim/ct-sim setup',
'soc ser - consult',
'soc ser - note',
'social service consult',
'social service note',
'spcs - program referral form',
'symptom assessment and intervention',
'tomo planned adaptive',
'tomo worksheet',
'tomotherapy distribution',
'tomotherapy lasers',
'treatment prescription',
'tumour board note',
]

def get_patient_list_db(parameters):

    sql_query = """SELECT DISTINCT  %s FROM %s WHERE %s \
    """ %(parameters['key'], parameters['database'], parameters['filter'])

    conn = pymssql.connect(
                host=parameters['host'],
                user=parameters['user'],
                password=parameters['password']
                )

    data = pd.read_sql_query(sql_query, conn)
    print data
    conn.close()

def read_patient_list_csv(patient_list, limit = None):
    patient_info = {}
    with open(patient_list, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = csv_reader.next()
        L = len(header)
        cnt = 0
        for title in header:
            patient_info[title] = [] 
        for row in csv_reader:
            row[0] = '{0:07d}'.format(int(row[0]))
            cnt += 1
            if cnt <= limit:
                for i in range(L):
                    patient_info[header[i]].append(row[i])

    return patient_info

def get_document_list(PatientId, download_params):
    patient = "%s/%s?PatientId=%s"%(MEDPHYS_API, DOCUMENT_PATH, PatientId)
    response  = requests.get(patient)
    if response.status_code == 200:
        #Store the contents of the website under doc
        doc = lh.fromstring(response.content)
        #Parse data that are stored between <tr>..</tr> of HTML
        tr_elements = doc.xpath('//tr')
        #Create empty list
        table = {}
        header = []
        i=0
        #For each row, store each first element (header) and an empty list
        for t in tr_elements[0]:
            i+=1
            name=t.text_content().strip()
            header.append(name)
            # print '%d:"%s"'%(i,name)
            table[name] = []

        # print len(tr_elements)   
        #Since out first row is the header, data is stored on the second row onwards
        for j in range(1,len(tr_elements)):
            #T is our j'th row
            T=tr_elements[j]
            
            #If row is not of size i, the //tr data is not from our table 
            if len(T)!= len(header):
                print 'Row does not have %d columns' %len(header)
            
            #i is the index of our column
            i=0
            
            #Iterate through each element of the row
            for t in T.iterchildren():
                data=t.text_content() 
                data = data.strip().lower()
                data = data.strip()
                #Append the data to the empty list of the i'th column
                if 'Creation Date' in header[i]:
                    datetime_object = datetime.strptime(data.strip(), '%b %d %Y %I:%M%p')
                    data = datetime_object.strftime("%Y%m%dT%H%M%S")
                elif 'Document Type' in header[i]:
                    if data in download_params['consult_notes']:
                        data = 'ConsultNote'
                    elif data in download_params['followup_notes']:
                        data = 'FollowUpNote'
                    elif data in download_params['end_of_treatment_notes']:
                        data = 'EndOfTrNote'
                    elif data in download_params['nursing_notes']:
                        data = 'nu_'+data
                    elif data in download_params['unknown_notes']:
                        data = 'UnKown_note'
                    elif data not in download_params['other_notes']:
                        print data
        
                table[header[i]].append(data)
                #Increment i for the next column
                i+=1
        # print [len(C) for (title,C) in table]
    else:
        print "ERROR getting: %s" %patient
    return table

def download_document(PatientId, file_name, label):
    # print 'Downloaded: \t %s \t %s'%(PatientId, label)
    document = "%s/%s/%s"%(MEDPHYS_API, V_FILEDATA, file_name)
    response  = requests.get(document)
    if response.status_code == 200:
        #Store the contents of the file into folder
        with open("%s/%s_%s"%(PatientId,label,file_name), 'wb') as f:
            f.write(response.content)

def main():
    parameters = {
            'server' : os.getenv("DB_SERVER"),
            'host' : os.getenv("DB_HOST"),
            'user' : os.getenv("DB_USER"),
            'password' : os.getenv("DB_PASSWORD"), 
            'database' : os.getenv("DB_DATABASES"),
            'key' :  os.getenv("DB_KEYS"),
            'filter' :  os.getenv("DB_FILTERS"),
            }
    # script to get patients from database according to the filter
    # patient_info = get_patient_list_db(parameters)

    # script to get patient from csv table
    patient_info = read_patient_list_csv(PATIENT_LIST_CSV, limit = 50)
    patient_note_path = os.getenv('PATIENT_NOTE_PATH')
    download_params = {
    'end_of_treatment_notes' : END_OF_TREATMENT_NOTES, 
    'consult_notes' : CONSULT_NOTES,
    'followup_notes' : FOLLOWUP_NOTES,
    'nursing_notes' : NURSING_NOTES,
    'unknown_notes' : UNK_NOTES,
    'other_notes' : OTHER_NOTES,
    }
    notes_to_download = ['ConsultNote', 'EndOfTrNote','FollowUpNote', 'UnKown_note']
    formats = ['.doc', '.docx', '.txt', '.dat']
    if 'PatientID' in patient_info:
        for PatientId in patient_info['PatientID']:
            patient_folder = "%s/%s"%(patient_note_path, PatientId)
            if not os.path.isdir(patient_folder):
                os.mkdir(patient_folder)

            print 'Downloading: \t %s' %PatientId
            doc_table = get_document_list(PatientId, download_params)
            for i in range(len(doc_table['Document Type'])):
                if doc_table['Document Type'][i] in notes_to_download:
                    extension = os.path.splitext(doc_table['Document Filename'][i])[1]
                    if extension in formats:
                        label = doc_table['Creation Date'][i]+'_'+doc_table['Document Type'][i]
                        download_document(patient_folder, doc_table['Document Filename'][i], label)
                    elif extension != '.pdf':
                        print 'skipped: %s \t format'%extension

            # print doc_table.keys()
    else:
        print 'PatientID not in patient_info keys %s'%patient_info.keys()



if __name__ == "__main__":
    main()