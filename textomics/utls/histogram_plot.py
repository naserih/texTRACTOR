#histogram_plot
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os
import csv

variable = ['f_words',  'f_lengh', 'f_lines'][1]

statFolder = r'C:\Users\FEPC-L389\Dropbox (Personal)\1_PhDProject\NLP\stats'
files = [os.path.join(statFolder,f) for f in os.listdir(statFolder) if '.csv' in f]
print (files)
# sns.set(color_codes=True)
# sns.palplot(sns.hls_palette(8, l=.3, s=.8))
labeles = []
plt.figure(figsize=(8,4))
plt.xlim((-10, 30000))
print(variable)
print('min max mean median std sem')
for file in files:
    dataframe = pd.read_csv(file)
    # print (dataframe.head())
    x = dataframe[variable]
    print(np.min(x), np.max(x), np.mean(x), np.median(x), np.std(x), stats.sem(x))
    # print (x)
    # sns.distplot(x)
    labeles.append(dataframe.columns[0])
    sns.distplot(x, kde=True,  label="bw: 2")
    # sns.kdeplot(x, shade=False, label=str(dataframe.columns[0]))

plt.legend(labels=labeles)
plt.title(variable)    

# sns.distplot(x);
# sns.distplot(x, hist=False, rug=True);

# from scipy.integrate import trapz
# density = np.sum(kernels, axis=0)
# density /= trapz(density, support)
# plt.plot(support, density);
# ;

# sns.kdeplot(x)
# sns.kdeplot(x, bw=.2, label="bw: 0.2")
# sns.kdeplot(x, bw=2, label="bw: 2")
# plt.legend()
# plt.show()

# x = np.random.gamma(6, size=200)
# sns.distplot(x, kde=False, fit=stats.gamma, label="bw: .2")
# sns.distplot(x, kde=False, fit=stats.gamma, label="bw: 2")
plt.show()

