# performance_check.py
import csv
import env

DATA_ROOT = env.DATA_ROOT

french_notes = [
]
nlp_score_file = 'ARIA_pain_score_NLP.csv'
inner_annotater_file = 'ARIA_inner_annotater.csv'
performance_out = 'ARIA_NLP_vs_Annotator_All.csv'
audit_score_files = [
                'ARIA_pain_score_S0.csv',
                'ARIA_pain_score_S1.csv',
                'ARIA_pain_score_S2.csv',
                'ARIA_pain_score_S3.csv', 
                'ARIA_pain_score_S4.csv',
                'ARIA_pain_score_S5.csv',
                    ]
# nlp_score = {}

pain_scores = {}
for audit_score_file in audit_score_files:
    with open(DATA_ROOT+audit_score_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ",")
        # header = next(csvreader)
        for row in csvreader:
            key = row[0].split('_')[1] 
            print(key)
            if key not in pain_scores:
                pain_scores[key] = {audit_score_file : row[1]}
            else:
                pain_scores[key][audit_score_file] = row[1]

 
# print(pain_scores)
with open(DATA_ROOT+nlp_score_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ",")
    header = next(csvreader)
    for row in csvreader:
        key = row[0].split('_')[1].split('.')[0]
        # nlp_score[key] = row[3]
        if key in pain_scores:
            pain_scores[key][nlp_score_file] = row[3]

# print(pain_scores)

score_scale = ['na', 'none', 'mild','moderate', 'severe']
# print (score_scale)


### EXPORT PERFORMANCE NLP vs ANNOTATOR
note_lang = ''
score = ''
with open(DATA_ROOT+performance_out, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ",")
    csvwriter.writerow(['note_ID', 'na', 'no-pain','pain', 'NLP_score'])
    for note in pain_scores:
        if note in french_notes:
            note_lang = '_FR'
        else:
            note_lang = '_EN'
     
        if nlp_score_file in pain_scores[note]:
            score_NLP = pain_scores[note][nlp_score_file]
        else:
            score_NLP ='NaN'
        score_RO = [0,0,0]
        for key in audit_score_files:
            if key in pain_scores[note]:
                if pain_scores[note][key] in ['mild','moderate', 'severe']:
                    score_RO[2]+= 1
                elif pain_scores[note][key] == 'none':
                    score_RO[1]+= 1
                elif pain_scores[note][key] == 'na':
                    score_RO[0]+= 1
                else:
                    print('ERROR: ', pain_scores[note][key])

        csvwriter.writerow([note+note_lang]+score_RO+[score_NLP])




#### EXPORT INNER ANNOTATOR AGREEMENT

note_lang = ''
with open(DATA_ROOT+inner_annotater_file, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ",")
    csvwriter.writerow(['note_ID']+score_scale+['NLP_score'])
    for note in pain_scores:
        if note in french_notes:
            note_lang = '_FR'
        else:
            note_lang = '_EN'

        score = [0,0,0,0,0]
        if len(pain_scores[note].keys()) > 4:
            if nlp_score_file in pain_scores[note]:
                score.append(pain_scores[note][nlp_score_file])
            else:
                score.append('NOT_IN_NLP')
            for key in audit_score_files:
                # print (key)
                # print 
                if key in pain_scores[note]:
                    score[score_scale.index(pain_scores[note][key])] += 1
                else:
                    print(note, pain_scores[note].keys())
            print ([note+note_lang]+ score)
            csvwriter.writerow(([note+note_lang]+score))



