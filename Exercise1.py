
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def handle_missingValues_simple(incomplete_data):

    complete_data = incomplete_data.fillna(method='bfill').fillna(method='ffill')
    return complete_data

def handle_outliers(noisy_data):

    cleaned_data=noisy_data
    for column in cleaned_data:
        cleaned_data[column] = cleaned_data[column].rolling(window=2,center=True).median().fillna(method='bfill').fillna(method='ffill')
    return cleaned_data


# In[5]:


productprices = pd.read_csv(open("data/market-prices-all-products_en.csv", "r"), encoding='utf-8', engine='c', header=0)
productprices=productprices.set_index('Country')
productprices=handle_missingValues_simple(productprices)
productprices=handle_outliers(productprices)
productprices.head()


# In[6]:


subset=productprices[(productprices["Product code"]=="254")][["Period","MP Market Price"]]
subset["Period"]=subset["Period"]/100
subset["Period"]=subset["Period"].apply(np.floor)

subset=subset.set_index('Period')
subset=subset.groupby(subset.index)['MP Market Price'].mean().reset_index()
subset=subset[(subset['Period']<2019)&(subset['Period']>2004)]


# In[7]:


privateUniversityStudents = pd.read_csv(open("data/OGD_uptstud_ext_UPT_S_1.csv", "r"), encoding='utf-8', engine='c', header=0,sep=";")
metadata=pd.read_csv(open("data/OGD_uptstud_ext_UPT_S_1_C-BER_ZEIT-0.csv", "r"), encoding='utf-8', engine='c', header=0,sep=";")


privateUniversityStudents=privateUniversityStudents.set_index("C-BER_ZEIT-0")
metadata=metadata.set_index("code")

privateUniversityStudents=privateUniversityStudents.join(metadata,how='inner').reset_index()
print(privateUniversityStudents.head())
privateUniversityStudents=privateUniversityStudents[2:]


# In[8]:


subset= subset.assign(PrivateStudents=pd.Series(privateUniversityStudents["F-STUDPG"]).values)


fig, ax1 = plt.subplots()
ax1 = subset.plot(x="Period", y="MP Market Price",ax=ax1,color='tab:blue')
ax1.set_ylabel('Butter Marked Price in €/100 kg', color='tab:blue')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2 = subset.plot(x="Period", y="PrivateStudents",ax=ax2,color='tab:red')
ax2.set_ylabel('Total Number of students at private universities', color='tab:red')
fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax2.legend(['Total Number of students at private universities'],loc=0)
ax1.legend(['Butter Marked Price'],loc=4)
plt.savefig('Figure.png', bbox_inches='tight')
plt.show()


# In[9]:


subset=subset.set_index('Period')
subset.to_csv('output.csv', sep=',', encoding='utf-8')

