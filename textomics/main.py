import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import time
from definitions import pain_dictionary, pain_terms
import env
# print(pain_dictionary)

def read_patient_doc(patient_file):

    if '.txt' in patient_file and '.doc' not in patient_file:
        with open(patient_file, 'r', encoding='utf-8',
            errors='ignore') as myfile:
            text = myfile.read()
    elif '.doc' in patient_file and '.txt' not in patient_file:
        text = textract.process(patient_file)
    else:
        print 'Error: file is unknown %s' %patient_file
        text = ''
    return text

def data_stats(input_files, output_files_path):
    # nlp = spacy.load('en_core_web_sm')
    f_lengh_list = []
    f_lines_list = []
    f_words_list = []
    print('%s files loaded'%len(input_files))
    with open('%s/records_stat.csv'%output_files_path, "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['input_file', 'f_size', 'f_lines','f_words', 'f_lengh'])
        for input_file in input_files:
            f_size = os.path.getsize(input_file)
            data = read_patient_doc(input_file)
            # doc = nlp(unicode(data, "utf-8"))
            # f_sentences = len([sent.string.strip() for sent in doc.sents])
            f_lines = len(data.split('\n'))
            f_lengh = len(data)
            f_words = len(data.split())
            csvwriter.writerow([os.path.basename(input_file), f_size, f_lines, f_words, f_lengh])

            f_lengh_list.append(int(f_lengh))
            f_lines_list.append(int(f_lines))
            f_words_list.append(int(f_words))
    return f_lengh_list, f_lines_list, f_words_list

def plot_pain_status(pain_status_path, pain_status_file):
    xmin = 0
    xmax = 1
    spacing = .1 
    bins = 3 # np.linspace(xmin, xmax, spacing)
    weights = [
    np.ones_like(pain_status_file[0]) / len(pain_status_file[0]),
    np.ones_like(pain_status_file[1]) / len(pain_status_file[1]),
    np.ones_like(pain_status_file[2]) / len(pain_status_file[2])
    ]
    print np.histogram(pain_status_file[0], bins)[0]
    print np.histogram(pain_status_file[1], bins)[0]
    print np.histogram(pain_status_file[2], bins)[0]
    # plt.hist(pain_status_file[0], weights=weights)
    # print bins
    plt.style.use('seaborn-deep')
    plt.rcParams['figure.figsize'] = [5, 5]
    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.grid(color='k', linestyle='-', axis='y', linewidth=.5, alpha = .3)
    ax.hist(pain_status_file, bins, alpha=.9, edgecolor='white', linewidth=1, 
        label=['i2b2', 'mimic-iii', 'aria'], weights=weights)
    ax.legend(loc='upper left')
    plt.ylim(top=.8)
    ax.xaxis.set_ticks(np.arange(-1, 1.1, 1))

    out_file = r'C:\Users\FEPC-L389\Google Drive\PhD_McGill\3_SUBMISSIONS\NLP_paper\pain_status.pdf'
    plt.savefig(out_file)

def plot_stat(f_lengh_list, f_lines_list, f_words_list):
    xmin = 0
    xmax = 40
    spacing = 100
    mu, std = norm.fit(f_lengh_list)
    # 
    bins = np.linspace(xmin, xmax, spacing)
    a = np.median(f_lengh_list)
    m = np.mean(f_lengh_list)
    p = norm.pdf(bins, mu, std)
    rv = gamma(a)
    rv2 = gamma(m)
    rv3 = gamma((m+a)/2)

    x_label = 20
    y_label = 20

    plt.rcParams['figure.figsize'] = [10, 5]

    plt.figure(0)
    plt.plot(bins, rv.pdf(bins), 'k-.', lw=2, label='Gamma distribution')
    plt.plot(bins, p, 'k--', linewidth=1.5, label='Gaussian distribution')
    plt.hist(f_lengh_list, bins, density=True, alpha=0.8, color = 'b', label='# of characters (#/1000)')
    plt.axvline(x=a, c="r")
    plt.axvline(x=m, c="orange")
    plt.text(x_label, 0.1, "Median = %i characters"%(int(a*1000)), fontsize=12, color = "r")
    plt.text(x_label, 0.08, "Mean = %i characters"%(int(m*1000)), fontsize=12, color = "orange")

    plt.legend(loc='upper right')
    plt.title("# of characters Histogram")
    plt.savefig('%s/02_histogram_fCharacters_gammaFit.pdf'%(output_files_path))
    plt.savefig('%s/02_histogram_fCharacters_gammaFit.png'%(output_files_path))

    plt.figure(1)
    plt.hist(f_lengh_list, bins, alpha=1, color = 'b', label='# of characters (#/1000)')
    # plt.plot(bins, p, 'k', linewidth=2)
    plt.axvline(x=np.mean(f_lengh_list), c="r")
    plt.text(x_label, y_label, "Mean = %i characters"%(int(np.mean(f_lengh_list)*1000)), fontsize=12, color = "r")

    plt.legend(loc='upper right')
    plt.title("# of characters Histogram")
    plt.savefig('%s/02_histogram_fCharacters.pdf'%(output_files_path))
    plt.savefig('%s/02_histogram_fCharacters.png'%(output_files_path))


    plt.figure(2)
    plt.hist(f_lengh_list, bins, alpha=0.1, color = 'k', label='# of characters (#/1000)')
    plt.hist(f_words_list, bins, alpha=0.8, color = 'g', label='# of words (#/100)')
    plt.axvline(x=np.mean(f_words_list), c="r")
    plt.text(x_label, y_label, "Mean = %i words"%(int(np.mean(f_words_list)*100)), fontsize=12, color = "r")

    plt.legend(loc='upper right')
    plt.title("#of words Histogram")
    plt.savefig('%s/02_histogram_fwords.pdf'%(output_files_path))
    plt.savefig('%s/02_histogram_fwords.png'%(output_files_path))

    plt.legend(loc='upper right')
    plt.title("# of sentences Histogram")
    plt.savefig('%s/02_histogram_fsents.pdf'%(output_files_path))
    plt.savefig('%s/02_histogram_fsents.png'%(output_files_path))

    plt.figure(4)
    plt.hist(f_lengh_list, bins, alpha=0.1, color = 'k' , label='# of characters (#/1000)')
    plt.hist(f_lines_list, bins, alpha=0.8, color = 'purple', label='# of lines (#/10)')
    # plt.hist(f_lines_list, bins, alpha=0.3, label='# of lines (#/20)')
    plt.axvline(x=np.mean(f_lines_list), c="b")
    plt.text(x_label, y_label, "Mean= %i lines"%(int(np.mean(f_lines_list)*10)), fontsize=12, color = "b")

    plt.legend(loc='upper right')
    plt.title("# of sentences Histogram")
    plt.savefig('%s/02_histogram_flines.pdf'%(filefolder))
    plt.savefig('%s/02_histogram_flines.png'%(filefolder))

def concat_temp(temp_file_path, mapped_file_path):
    temp_files = os.listdir(temp_file_path)
    batches = {}
    for temp_file in temp_files:
        if temp_file.split("_")[1] in batches:
            batches[temp_file.split("_")[1]].append(temp_file)
        else:
            batches[temp_file.split("_")[1]] = [temp_file]
    for key, filenames in batches.items():
        print('concat_%s.txt'%(key))
        with open(os.path.join(mapped_file_path,'concat_%s.txt'%(key)), 'w') as outfile:
            for fname in filenames:
                with open(os.path.join(temp_file_path, fname)) as infile:
                    outfile.write(infile.read())
            
def qc_metamaped(input_file, mapped_files_path):
    USER = ['processing 00000000.tx', 'processing user.tx']
    mapped_files = os.listdir(mapped_files_path)
    # mapped_files = ['_'.join(f.split(".")[0].split("_")[:-1]) for f in os.listdir(mapped_files_path)]
    
    print mapped_files
    print os.path.basename(input_file)
    for mapped_file in mapped_files:
        validRecord = 0
        print (input_file, mapped_file)
        if input_file in mapped_file:
            with open(os.path.join(mapped_file_path,mapped_file), 'r') as f:
                        reader = f.readlines()
                        processed_data = []
                        for line in reader:
                            line = line.strip().lower()
                            if USER[0] in line or USER[1] in line:
                                validRecord = 1
    return validRecord

def export_metamaped_table(mapped_file_path,metamapped_output):
    conditionals = [' if ','.if ', ' when,', ' if,', ' in case of ', ' in case ',' before ', 
                    ' whether',' might ', 'may ', ' as needed  ', 'possibil', 'possible'
     ' would ',' could ',  ' should ', ' history', ' historical', ' previously ', ' previous ' ,
     ' in the last ', ' prior ', ' recent years ', ' call ', ' please ', ' seek ', ' p.r.n.', ' return ', ' in the past']
    nonconditionals = [ ' since ', ' control',  'present', ' current',' now ', 'report', ' now,', ' treated', ' because of ', ' where, ', ' where ', ' lasted ', 
                       ' resolved ', ' found ', ' controll',' treated ' ,' prevent', ' manage', ' confort',' diagnosis ', 
                       'severe', 'worsening', 'aggravated', 'diffuse '
                       'severity', 'increased', 'score', 'hight', 'mild', 'modorate']
    drug_excludes = ["'his ", "'f- ", "'lead ", "histidine", "prevent", "wake", "level",
                   "helium","dob"
                    ]
    confirmed_nopains = ['nontender', 'non-tender', 'non tender']
    pain_abr_lookup_dic = {' cp ':' chest pain ', ' akp ':' anterior knee pain ', ' lbp ':' low back pain '}
    mapped_files = os.listdir(mapped_file_path)
    senstence_database = {}
    globalcnt = 0
    concepts = []
    with open(metamapped_output+'_OUT_mapped.csv', "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['file','sentence', 'phrase', 'sentenceindex','phraseindex','mappingindex',
                            'score','nagation','conditional_s','conditional', 'drug_s','drug',
                            'concept_id','concept_name','concept_type'])
        cnt = 0
        # USER = 'processing user.tx'
        USER = 'processing 00000000.tx'
        for mapped_file in mapped_files:
            cnt += 1
            print (cnt, mapped_file)
            defult = " "
            with open(os.path.join(mapped_file_path,mapped_file), 'r') as f:
                reader = f.readlines()
                processed_data = []
                sentenceindex = 0
                for line in reader:
                    line = line.strip().lower()
                    # print(line)
                    if USER in line:
                        sentenceindex += 1
                        phraseindex = 0
#                         line = line.replace('processing 00000000.tx.','')
                        sentense = line.replace(USER, '')
                        sentense = sentense.replace('|','')
                        sentense = sentense.replace('   ',' ')
                        sentense = sentense.replace('  ',' ')
                        sentense = sentense.replace('  ',' ')
#                         0_mapped_file, 1_sentense, 2_sentenceindex,3_#pain,4_#nopain,5_#cond,6_#abr,7_#conj,8_#drug, 
                        # 9_[pains], 10_[nopains], 11_[conds], 12_[abrs], 13_[drugs]
                        if globalcnt > 0:
                            senstence_database[globalcnt][3] = num_pain
                            senstence_database[globalcnt][4] = num_npain           
                            senstence_database[globalcnt][5] = num_cond
                            senstence_database[globalcnt][6] = num_abrv
                            senstence_database[globalcnt][7] = num_conj 
                            senstence_database[globalcnt][8] = num_drug
                        
                        globalcnt += 1
#                         print (mapped_file, sentense, sentenceindex,0,0,0,0,0,0, [], [], [], [], [])
                        senstence_database[globalcnt]=[mapped_file, sentense, sentenceindex,0,0,0,0,0,0, [], [], [], [], []]
                        conditional_s = 0
                        drug_s = 0
                        drugCancel = 0
                        num_drug = 0
                        num_cond = 0
                        num_abrv = 0
                        num_pain = 0
                        num_npain = 0
                        num_conj = 0
                        cond_tag = 1
                        for ncn in nonconditionals:
                            if ncn in sentense:
                                drugCancel = 1
                                cond_tag = 0
                        if cond_tag == 1:
                            for cn in conditionals:
                                if cn in sentense:
                                    num_cond += 1
    #                                 print('>>>>s ',cnt, sentenceindex, phraseindex, cn, '\n',phrase, '\t>>\t',sentense  )
                                    conditional_s = 1
                                    if cn not in  senstence_database[globalcnt][11]:
                                        senstence_database[globalcnt][11].append(cn)
                        for abr in pain_abr_lookup_dic:
                            if abr in sentense:
                                num_abrv += 1
#                                 print('>>>>s ',cnt, sentenceindex, phraseindex, cn, '\n',phrase, '\t>>\t',sentense  )
                                if abr not in  senstence_database[globalcnt][12]:
                                    senstence_database[globalcnt][12].append(abr)
                                
#                         print(sentenceindex, len(sentense))
#                         if len(sentense) < len(defult):
#                             sentense = defult
# #                             print temp_file
#                         defult = sentense
                    if 'phrase:' in line:
                        line = line.replace('phrase:','')
                        phraseindex += 1
                        mappingindex = 0
                        phrase = line
                        drug_tag = 0
                        conditional = 0
                        for cn in conditionals:
                            if cond_tag ==1 and (cn in phrase or ' please ' in sentense or ' if ' in sentense):
#                                 print('>>>>> ',cnt, sentenceindex, phraseindex, cn, '\n',phrase, '\t>>\t',sentense  )
                                conditional = 1
                    
                    if 'meta mapping' in line:
                        mappingindex += 1
                    
                    if line.find("[") > 0 and line.find("]")>0:
                        if line[line.find("["):line.find("]")+1] not in concepts:
                            concepts.append(line[line.find("["):line.find("]")+1])

                    if ( 'distress' in line and line.find('[')>0 and line.find('[sign or symptom]')<=0):
                        line = line.replace(line[line.find("["):line.find("]")+1],'')
                        d_type = "distress"

                    elif (USER not in line and line.find('[sign or symptom]')>0):
                        line = line.replace('[sign or symptom]','')
                        d_type = "sign or symptom"
                        # print('2_', line)
#                       print ("ss_HERE")
                    elif (USER not in line and (line.find('pharmacologic substance')>0 or line.find('clinical drug')>0)):
                        line = line.replace(line[line.find("["):line.find("]")+1],'')
                        d_type = "pharmacologic substance"
#                         print ("ps_HERE")
#                         print(line)

                        
                        if drugCancel == 0:
                            drug_tag = 1
                            drug_s = 1
                            num_drug += 1
                        else:
                            drug_tag = 0
                            drug_s = 0
                    # elif (USER not in line and line.find('disease or syndrome')>0):
                    #     line = line.replace(line[line.find("["):line.find("]")+1],'')
                    #     d_type = "disease or syndrome"
#                         print ("ds_HERE")
                    # elif (USER not in line and line.find('neoplastic process')>0):
                    #     line = line.replace('[neoplastic process]','')
                    #     d_type = "neoplastic process"
#                         print ("np_HERE")
                    # elif (USER not in line and line.find('[quantitative concept]')>0):
                    #     line = line.replace('[quantitative concept]','')
                    #     d_type = "quantitative concept"
#                         print ("qc_HERE")
                    # elif (USER not in line and line.find('[')>0 and 'report_end' not in line and ':' in line):
                    #     d_type = line[line.find("[")+1:line.find("]")]
                    #     line = line.replace(line[line.find("["):line.find("]")+1],'')
#                         print ("re_HERE")
                    else:
#                         print ("cn_HERE")
                        continue
                    score = (line[0:line.find(" ")].strip()).strip()
#                     print (score)
                    concept_id = (line[line.find(" "):].split(":")[0]).replace(" e ","").strip()
                    Negated = 0
#                     print (concept_id)
                    if concept_id.split(" ")[0] == "n":
                        Negated = 1
                        concept_id = concept_id.split(" ")[1] 
#                         print (line)
                    try:
                        concept_name = (line[line.find(" "):].split(":")[1]).strip()
                        # print (line, concept_name)
                    except:
                        print("GARBISH >>>", line)
                        concept_name = 'GARBISH'
#                     print Negated
#                     print (concept_name)
#                     print (str(score) + "\t" +  str(Negated) + "\t" + concept_id + "\t" + concept_name + "\t" + d_type)
                    sentense = sentense.replace('%','')
                    sentense = sentense.replace('(',' ')
                    sentense = sentense.replace(')',' ')
                    sentense = sentense.replace('[',' ')
                    sentense = sentense.replace(']',' ')
                    sentense = sentense.replace('{',' ')
                    sentense = sentense.replace('}',' ')
                    sentense = sentense.replace('   ',' ')
                    sentense = sentense.replace('  ',' ')
                    sentense = sentense.replace('  ',' ')
                    for confirmed_nopain in confirmed_nopains:
                        if confirmed_nopain in sentense:
                            senstence_database[globalcnt][10].append(concept_name)
                            num_npain += 1 
                    if d_type == "sign or symptom":
                        for pain_term in pain_terms:
                            if pain_term in concept_name:
                                if Negated == 0:
                                    if  concept_name not in senstence_database[globalcnt][9]:
                                        senstence_database[globalcnt][9].append(concept_name)
                                        num_pain += 1
                                if Negated == 1:
                                    if  concept_name not in senstence_database[globalcnt][10]:
                                        senstence_database[globalcnt][10].append(concept_name)
                                        num_npain += 1      
                    if d_type == "distress":
                        if Negated == 1:
                            if  concept_name not in senstence_database[globalcnt][10]:
                                senstence_database[globalcnt][10].append(concept_name)
                                num_npain += 1              
                    if d_type == "pharmacologic substance":
                        drug_tag = 1
                        for drug_exclude in drug_excludes:
                            if drug_exclude in concept_name:
                                drug_tag = 0
                        if  concept_name not in senstence_database[globalcnt][13] and drug_tag == 1:
                            senstence_database[globalcnt][13].append(concept_name)
                    datarow = [sentense, phrase,sentenceindex, phraseindex,
                            mappingindex, score, Negated,conditional_s, 
                            conditional,drug_s, drug_tag, concept_id, 
                            concept_name, d_type]    
                    csvwriter.writerow([mapped_file]+datarow)
                    # processed_data.append()
            # processed_data = set(processed_data)
#             for data in processed_data:
# #                 if 'pain' in data[0] and data[10] ==1:
# #                     print(data[2], data[9], data[10], '\t', data[1], '\n',data[0] )
#                 csvwriter.writerow([mapped_file]+data)
    splitted_data = {}
    with open(metamapped_output+'_OUT_map_sum_stat.csv', "wb",) as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['0_mapped_file', '1_sentense', '2_sentenceindex','3_#pain','4_#nopain',
                            '5_#cond','6_#abr','7_#conj','8_#drug', 
                        '9_[pains]',' 10_[nopains]',' 11_[conds]', '12_[abrs]', '13_[drugs]'])
        for key in senstence_database:
            row = senstence_database[key]
            # print row
            csvwriter.writerow(row)
            if row[0] in splitted_data:
                splitted_data[row[0]].append(row)
            else:
                splitted_data[row[0]]=[row]
    
    for key in splitted_data:
        with open(metamapped_output+key+'_map.csv', "wb",) as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['0_mapped_file', '1_sentense', '2_sentenceindex','3_#pain','4_#nopain',
                            '5_#cond','6_#abr','7_#conj','8_#drug', 
                        '9_[pains]',' 10_[nopains]',' 11_[conds]', '12_[abrs]', '13_[drugs]'])
            csvwriter.writerows(splitted_data[key])
    for concept in concepts:
        print concept 
def sentences_only(selected_output):
    files = os.listdir(selected_output)
    for f in files:
        with open(selected_output+f, "r") as csvfile:
            reader = csv.reader(csvfile)
            with open(selected_output+'_OP_'+f, "wb",) as csvout:
                csvwriter = csv.writer(csvout, delimiter=',')
                csvwriter.writerow(['sentense','0_no pain', '1_pain', 'irrelevant'])
                for row in reader:
                    # print row
                    csvwriter.writerow([row[1]])

'''
0_mapped_file   1_sentense  2_sentenceindex 3_#pain 4_#nopain   5_#cond 6_#abr  
7_#conj 8_#drug 9_[pains]    10_[nopains]    11_[conds] 12_[abrs]   13_[drugs]
'''
def get_pain_class(selected_output, filesrc):
    files = [f for f in os.listdir(selected_output) if 'OUT_' not in f and '_PAIN_' not in f]
    with open(selected_output+filesrc+'_PAIN_ALL.csv', "wb") as csvallout:
        allcsvwriter = csv.writer(csvallout, delimiter=',')
        allcsvwriter.writerow(['patient', 'sentense','pain Score'])
        for f in files:
            with open(selected_output+f, "r") as csvfile:
                reader = csv.reader(csvfile)
                reader.next()
                with open(selected_output+filesrc+'_PAIN_'+f, "wb") as csvout:
                    csvwriter = csv.writer(csvout, delimiter=',')
                    csvwriter.writerow(['sentense','pain Score'])
                    for row in reader:
                        # print len(row)
                        if len(row[13])>2 or len(row[11])>2:
                            if len(row[9])>2 or len(row[10])>2:
                                score = '-'
                            else:
                                score = ''
                        else:
                            if len(row[9])>2 and len(row[10])>2:
                                score = 10
                            elif len(row[9])>2:
                                score = 1
                            elif len(row[10])>2:
                                score = 0
                            else:
                                score = ''

                        csvwriter.writerow([row[1], score])
                        allcsvwriter.writerow([f,row[1], score])


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
def check_pains(concept, catagory):
    is_pain = False
    for term in pain_terms:
        if term.strip() in concept and 'cachexia' not in concept:
            is_pain = True
            s_t = term
            pain_concept = concept.strip()
    if is_pain:
        if pain_concept in pain_dictionary:
            return pain_dictionary[pain_concept]
            pass
        elif catagory != 'sign or symptom':
                pass
        else:
            print pain_concept, s_t
            pass
    else:
        if concept.strip() in pain_dictionary:
            print 'ERROR in pain:', concept
def filter_pains(map_file_path):
    pain_classes = []
    with open(map_file_path, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = csv_reader.next()
        for row in csv_reader:
            if len(row) != 15:
                print 'ERROR'
            elif row[11][0] != 'c':
                term = row[13]
                catagory = row[14]
                if len(row[11]) > 1:
                    print row[11]
            else:
                term = row[12]
                catagory = row[13]
            # print term, catagory
            pain_class = check_pains(term, catagory)
            if pain_class:
                pain_classes.append([pain_class])
    return pain_classes
        

def main():
    set_name = env.SET_NAME
    filesrc = env.FILE_SRC
    metamap_path = env.METAMAP_ROOT
    data_root = env.DATA_ROOT
    output_files_path = "%s/metamap_pain"%(data_root)
    # metamap_cache_path = "%s/metamap_cache"%(data_root)
    metamap_conc_path = [
            r'C:\hossein\NLP_local\DS1_i2b2_train_test_released_20090817\mapped/'+set_name,
            r'C:\hossein\NLP_local\DS3_MIMIC-III_NOTEEVENTS_old\mapped/'+set_name,
       "%s/metamap_conc"%(data_root)
            ][dbi]
    # # print('DONE!')
    # if not os.path.isdir(output_files_path):
    #     os.mkdir(output_files_path)
    # patients_docs_root = '/var/www/devDocuments/hossein/Galenus/data/notes/TS_MET_notes'
    # patients_docs_path = [os.path.join(patients_docs_root, f) for f in 
    #                         os.listdir(patients_docs_root)]
    # print (filepath)

    # fileType = ['ConsultNote', 'EndOfTrNote', 'FollowUpNote', 'UnKown_note'][0]
    # patients_docs = []
    # for patient_docs in patients_docs_path:
    #     # print os.listdir(patient_docs) 
    #     word_documents = [os.path.join(patient_docs,f) for f in os.listdir(patient_docs) if f.endswith('.doc') and fileType in f]
    #     patients_docs += word_documents

    # f_lengh_list, f_lines_list, f_words_list = data_stats(patients_docs, output_path)
    # plot_stat(f_lengh_list, f_lines_list, f_words_list) 
    # for patients_doc in patients_docs:
    #     # print os.path.basename(patients_doc)
    #     print (patients_doc)
    #     textdata = read_patient_doc(patients_doc)
        # print(textdata)
        # process_metamap(patients_doc, textdata,metamap_cache_path, metamap_path)
        # while qc_metamaped(patients_doc, metamap_cache_path)==0:
            # print ('Error: QC Failed')
            # process_metamap(patients_doc, textdata,metamap_cache_path, metamap_path)
                    # time.sleep(30)


    # concat_temp(metamap_cache_path, metamap_conc_path)
    metamapped_output_file = "%s/%s/%s/"%(output_files_path,filesrc, set_name)
    selected_files = metamapped_output_file
    if not os.path.isdir(selected_files):
        os.mkdir(selected_files)
    # print(metamapped_output_file)
    
    export_metamaped_table(metamap_conc_path, metamapped_output_file)
    get_pain_class(selected_files, filesrc)
    # map_file = [r'\i2b2', r'\mimic', r'\AREA'][2]
    # map_root = r'C:\Users\FEPC-L389\Dropbox (Personal)\1_PhDProject\Galenus\data\metamap_pain'
    # map_file_path = map_root+map_file+'_maped.csv'
    # pain_classes = filter_pains(map_file_path)
    # with open(map_file_path+'classes.csv', 'wb') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerows(pain_classes)
    # pain_status_path = r'C:\Users\FEPC-L389\Dropbox (Personal)\1_PhDProject\Galenus\data\metamap_pain\pain_status_table.csv'
    # pain_status_file = [[],[],[]]
    # with open(pain_status_path, 'rb') as csvfile:
    #     csvreader = csv.reader(csvfile)
    #     csvreader.next()
    #     for row in csvreader:
    #         if row[3] != '':
    #             pain_status_file[0].append(float(row[3]))
    #         if row[7] != '':
    #             pain_status_file[1].append(float(row[7]))
    #         if row[11] != '':
    #             pain_status_file[2].append(float(row[11]))
    # plot_pain_status(pain_status_path, np.array(pain_status_file))
if __name__ == "__main__":
    main()