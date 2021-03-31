import os
import time
import textract
import env

def extract_patient_note(patient_file):

    if '.txt' in patient_file and '.doc' not in patient_file:
        with open(patient_file, 'r', encoding='utf-8',
            errors='ignore') as myfile:
            text = myfile.read()
    elif '.doc' in patient_file and '.txt' not in patient_file:
        text = textract.process(patient_file)
    else:
        print ('Warning: file %s processed as txt.' %patient_file)

        with open(patient_file, 'rb') as myfile:
            text = myfile.read()
    return text

def process_metamap(input_file, data, temp_file, meta_file):
    if not os.path.exists(temp_file):
        os.makedirs(temp_file)
    batch_max_size = 7500
    data = "".join(i for i in data if ord(i)<128)
    data = data.replace('"', '')
    data = data.replace("'", '')
    data = data.replace("%", '')
    lines = data.split('\n')
    batch_data = data.replace('\n', ' ')
    # print('ICI MADAMME!!')
    n_line_len = 0
    cut_i = 0
    cut_f = 0
    batch_n = 0
    if len(batch_data) > batch_max_size:
        for line in lines:
            n_line_len += len(line)
#                 print '>>>>>>>>>>', batch_n, p_cut, n_cut, len(lines), p_line_sum, n_line_len
            if n_line_len > batch_max_size or cut_f+1 == len(lines):
                if cut_i+1 == len(lines):
                    cut_f = cut_f+1
#                     print os.path.basename(input_file), f_lengh, '>>>>>>>>>>',batch_n, p_cut, n_cut, len(lines), p_line_sum
                batch_data = ' '.join(lines[cut_i:cut_f])
#                     if len(batch_data) > 7999:
#                         print '***********************************************************'
#                     print os.path.basename(input_file), batch_n, len(batch_data)
                outputfilepath = temp_file +'/batch_'+ os.path.basename(input_file)+'_'+str(batch_n) + '.txt'
                if os.path.isfile(outputfilepath):
#                         print 'Already in Downoloads!', os.path.basename(outputfilepath)
                    pass
                else:
#                         print outputfilepath
                    os.system('echo "' + batch_data + '" | ' + meta_file + ' --prune 100  -I --negex > "' + outputfilepath +'"')
                    if os.path.isfile(outputfilepath):
                        pass
                        print ('SUCCESSFULY PROCESSED!', os.path.basename(outputfilepath))
                    else:
                        print ('>>> ERROR: NOT PROCESSED!', os.path.basename(outputfilepath))
                        print(len(batch_data))
                batch_n += 1
                cut_i = cut_f
                n_line_len =  len(line)
            cut_f += 1
    else:
        outputfilepath = temp_file +'/batch_'+ os.path.basename(input_file)+'_'+str(batch_n) + '.txt'
        if os.path.isfile(outputfilepath):
#                 print 'Already in Downoloads!', os.path.basename(outputfilepath)
            pass
        else:
#                 print outputfilepath
            os.system('echo "' + batch_data + '" | ' + meta_file + ' --prune 100  -I --negex > "' + outputfilepath +'"')
            if not os.path.isfile(outputfilepath):
                print ('>>> ERROR: NOT PROCESSED!', os.path.basename(outputfilepath))
                print(len(batch_data))
#                     print batch_data
            else:
                print ('SUCCESSFULY PROCESSED!', os.path.basename(outputfilepath))
                pass
#                 os.system('echo "' + batch_data + '" | ' + meta_file + ' --prune 100  -I --negex > "' + temp_file +'\\batch_'+ os.path.basename(input_file)+'_'+str(batch_n)  + '.txt"')
#                 print 1000000, 'echo "'  + '" | ' + meta_file + ' --prune 100  -I --negex > "' + temp_file +'\\batch_'+ os.path.basename(input_file)+'_'+str(batch_n)  + '.txt"'
#                 print 2000000, 'echo "'  + '" | ' + meta_file + ' --prune 100  -I --negex > "' + outputfilepath +'"'
            
#                 print os.path.basename(input_file), batch_n, len(batch_data)

def main():
    project_root = env.ROOT
    documents_root = project_root+r'\TEST_notes\txt Examples'
    metamap_cache_path = "%s/metamap_cache"%(project_root)
    metamap_path = env.METAMAT_APP
    patients_folders = [os.path.join(documents_root, patient) for patient in 
                            os.listdir(documents_root)]

    print (patients_folders)
    '''
    fileType: if specific file type need to be filtered
    fileFormat: this route accepts '.txt', '.doc' formats. 
    If file format is not specified it will be processed as 'txt' file
    '''
    fileType = ['','ConsultNote', 'EndOfTrNote', 'FollowUpNote', 'UnKown_note'][0]
    fileFormat = ['', '.doc'][0]
    all_patients_files = []
    for patient_folder in patients_folders:
        # print os.listdir(patient_folder) 
        patient_files = [os.path.join(patient_folder,patient_file) for patient_file in os.listdir(patient_folder) if patient_file.endswith(fileFormat) and fileType in patient_file]
        all_patients_files += patient_files
    # print (all_patients_files)
    # f_lengh_list, f_lines_list, f_words_list = data_stats(patients_docs, output_path)
    # plot_stat(f_lengh_list, f_lines_list, f_words_list) 
    for patient_note in all_patients_files:
        # print os.path.basename(patients_doc)
        print (patient_note)
        textdata = extract_patient_note(patient_note)
        print(textdata)
        process_metamap(patient_note, textdata,metamap_cache_path, metamap_path)
        # while qc_metamaped(patient_note, metamap_cache_path)==0:
        #     print ('Error: QC Failed')
        #     process_metamap(patient_note, textdata,metamap_cache_path, metamap_path)
        #     time.sleep(30)

if __name__ == "__main__":
    main()