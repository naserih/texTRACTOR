#split_train_test.py
import os
import shutil
import random
import numpy as np

src_folder_path = '../data/pdfs/TS_MET_notes/ALL/'
out_sets = [
'../data/pdfs/TS_MET_notes/SET0/',
'../data/pdfs/TS_MET_notes/SET1/',
'../data/pdfs/TS_MET_notes/SET2/',
'../data/pdfs/TS_MET_notes/SET3/',
'../data/pdfs/TS_MET_notes/ARCHIVE/'
]
out_set = '../data/pdfs/TS_MET_notes/REDO/'

# for file_path in out_sets:
#     if os.path.isdir(file_path):
#         shutil.rmtree(file_path)
# os.mkdir(out_set)
src_file_names = os.listdir(src_folder_path)

redo_files = [
'20181005T105800',
'20191016T131500',
'20191127T090100',
'20180228T095800',
'20180502T153500',
'20180410T142400',
'20191021T134200',
'20180404T182400',
'20180118T160300',
'20191104T144200',
'20180823T123700',
'20190528T125900',
'20190517T091600',
'20191023T101600',
'20191107T121800',
'20190326T114200',
'20180927T111500',
'20181227T195900',
'20180823T094900',
'20190315T105500'
]
# random.shuffle(src_file_names)

for file_name in src_file_names:
    # print()
    if file_name.split('_')[1] in redo_files:
        print(file_name.split('_')[1])
        shutil.copy(src_folder_path+file_name, out_set + file_name)

# cnt = 1
# for file_name in src_file_names:
#     if not os.path.exists(out_set + file_name):
#         print (cnt)
#         cnt+=1
#         shutil.copy(src_folder_path+file_name, out_set + file_name)
# print(src_file_names)
# patient_ids = [f.split("_")[0] for f in src_file_names]
# note_date = [int((f.split("_")[1])[:8]) for f in src_file_names]
# print(note_date)
# cnt = 0
# set0_patients = []
# for i in range(len(src_file_names)):
#     if cnt < 50 and note_date[i] > 20180000 and patient_ids[i] not in set0_patients:
#         print (cnt)
#         cnt += 1
#         set0_patients.append(patient_ids[i])
#         shutil.copy(src_folder_path+src_file_names[i], out_sets[0] +src_file_names[i])
#     elif cnt < 100 and note_date[i] > 20180000 and patient_ids[i] not in set0_patients:
#         print (cnt)
#         cnt += 1
#         set0_patients.append(patient_ids[i])
#         shutil.copy(src_folder_path+src_file_names[i], out_sets[1] +src_file_names[i])
#     elif cnt < 150 and note_date[i] > 20180000 and patient_ids[i] not in set0_patients:
#         print (cnt)
#         cnt += 1
#         set0_patients.append(patient_ids[i])
#         shutil.copy(src_folder_path+src_file_names[i], out_sets[2] +src_file_names[i])

#     elif cnt < 300 and note_date[i] > 20180000 and patient_ids[i] not in set0_patients:
#         print (cnt)
#         cnt += 1
#         set0_patients.append(patient_ids[i])
#         shutil.copy(src_folder_path+src_file_names[i], out_sets[3] +src_file_names[i])
#     else:
#         # print (cnt)
#         # set0_patients.append(patient_ids[i])
#         shutil.copy(src_folder_path+src_file_names[i], out_sets[4] +src_file_names[i])



# # for shuffle_file_name in shuffle_file_names[:50]:
# #     shutil.move(src_folder_path+shuffle_file_name, out_0_folder_path +shuffle_file_name)

# # for shuffle_file_name in shuffle_file_names[50:100]:
# #     shutil.move(src_folder_path+shuffle_file_name, out_1_folder_path +shuffle_file_name)
