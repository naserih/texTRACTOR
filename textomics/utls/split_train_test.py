#split_train_test.py
import os
import shutil
import random
import numpy as np

# src_folder_path = r'C:\hossein\NLP_local\DS1_i2b2_train_test_released_20090817'
# out_folder_path = r'C:\Users\FEPC-L389\Dropbox (Personal)\1_PhDProject\Galenus\data\metamap_pain\i2b2'

src_folder_path = r'C:\hossein\NLP_local\DS3_MIMIC-III_NOTEEVENTS_old'
out_folder_path = r'C:\Users\FEPC-L389\Dropbox (Personal)\1_PhDProject\Galenus\data\metamap_pain\mimic'
src_file_names = os.listdir(src_folder_path+r'\mapped')
scored_file_names = os.listdir(out_folder_path+r'\pain_score')
metamapped_file_names = os.listdir(out_folder_path+r'\metamapped')

if len(src_file_names) != len(scored_file_names) or len(src_file_names) != len(metamapped_file_names):
    print ('ERROR, ', len(src_file_names), len(scored_file_names), len(metamapped_file_names))
'''
tag can be defined to get the file ID
'''
src_file_tags = [f.split('.')[0] for f in os.listdir(src_folder_path+r'/mapped')]
scored_file_tags = [f.split('.')[0][6:] for f in os.listdir(out_folder_path+r'/pain_score')]
metamapped_file_tags = [f.split('.')[0] for f in os.listdir(out_folder_path+r'/metamapped')]

# print (metamapped_file_tags)

for i in range(len(src_file_tags)):
    if src_file_tags[i] != scored_file_tags[i]:
        print('ERROR')
    if src_file_tags[i] != metamapped_file_tags[i]:
        print('ERROR')

# os.mkdir(src_folder_path+r'/train')
# os.mkdir(src_folder_path+r'/test')
# os.mkdir(src_folder_path+r'/validation')
# os.mkdir(out_folder_path+r'/train')
# os.mkdir(out_folder_path+r'/train/pain_score')
# os.mkdir(out_folder_path+r'/train/metamapped')
# os.mkdir(out_folder_path+r'/test')
# os.mkdir(out_folder_path+r'/validation')
# os.mkdir(out_folder_path+r'/test/metamapped/')
# os.mkdir(out_folder_path+r'/validation/metamapped/')
# os.mkdir(out_folder_path+r'/test/pain_score/')
# os.mkdir(out_folder_path+r'/validation/pain_score/')

sampling_indxs = [i for i in range(len(src_file_names))]
# print(sampling_indxs)
random_file_indxs = random.sample(sampling_indxs, 5)


# random_file_indxs = [0]
set_name = '/train/'
# for k in random_file_indxs:
#     shutil.move(src_folder_path+r'/mapped/'+src_file_names[k], src_folder_path+set_name+src_file_names[k])
#     shutil.move(out_folder_path+'/metamapped/'+metamapped_file_names[k], out_folder_path+set_name+'metamapped/'+metamapped_file_names[k])
#     shutil.move(out_folder_path+'/pain_score/'+scored_file_names[k], out_folder_path+set_name+'pain_score/'+scored_file_names[k])