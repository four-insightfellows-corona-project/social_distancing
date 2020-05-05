#!/usr/bin/env python
# coding: utf-8

# # Goal:
# Train a simple model on the MVP dataset

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
sns.set()
get_ipython().run_line_magic('matplotlib', 'notebook')

data_path = os. getcwd()[:-9] +'Data/'


# In[2]:


df =  pd.read_csv(data_path+'df_mvp.csv')
df.time_bin = pd.to_datetime(df.time_bin)


# In[3]:


df.head(3)


# ## Train a logistic regression model

# In[4]:


from sklearn.model_selection import train_test_split
X = df.iloc[:,3:]
y = df.label
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


# In[5]:


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0,solver ='liblinear', penalty='l1').fit(X_train, y_train)


# In[6]:


from sklearn.metrics import classification_report

predictions = clf.predict(X_test)
# print(classification_report(y_test,predictions))


# In[7]:


from sklearn.metrics import roc_auc_score, roc_curve

def roc_auc(model,model_name, X_test, y_test):
    # generate a no skill prediction (majority class)
    ns_probs = [0 for _ in range(len(y_test))]
    # predict probabilities
    lr_probs = model.predict_proba(X_test)
    # # keep probabilities for the positive outcome only
    lr_probs = lr_probs[:, 1]
    # calculate scores
    ns_auc = roc_auc_score(y_test, ns_probs)
    lr_auc = roc_auc_score(y_test, lr_probs)
    # summarize scores
    # print('No Skill: ROC AUC=%.3f' % (ns_auc))
    # print(model_name+': ROC AUC=%.3f' % (lr_auc))
    # calculate roc curves
    ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
    lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
    # plot the roc curve for the model
    # plt.figure()
    # plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
    # plt.plot(lr_fpr, lr_tpr, marker='.', label=model_name)
    # # axis labels
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.legend(); plt.show()


# In[8]:


roc_auc(clf,'clf', X_test, y_test)


# In[9]:


sorted(list(zip(X.columns,clf.coef_[0])), key = lambda x: x[1],reverse=True) 


# ## upsample both labels

# In[10]:


from sklearn.utils import resample

n_target = 1000
# Separate majority and minority classes
df_mj = df[df.label==0] # safe
df_mi = df[df.label==1] # unsafe
 
# Upsample minority class, with replacement 
df_mi_up = resample(df_mi, replace=True, n_samples=n_target, random_state=101) 
df_mj_up = resample(df_mj, replace=True, n_samples=n_target, random_state=101) 
 
# Combine majority class with upsampled minority class
df_up= pd.concat([df_mj_up, df_mi_up])
 
# Display new class counts
df_up.label.value_counts()


# In[11]:


X_up = df_up.iloc[:,3:]
y_up = df_up.label

X_train_up, X_test_up, y_train_up, y_test_up = train_test_split(X_up, y_up, test_size=0.33, random_state=42)

clf_up = LogisticRegression(random_state=0,solver ='liblinear', penalty='l1').fit(X_train_up, y_train_up)


# In[12]:


predictions_up = clf_up.predict(X_test_up)
# print(classification_report(y_test_up,predictions_up))


# In[13]:


roc_auc(clf_up,'clf_up', X_test_up, y_test_up)


# In[14]:


sorted(list(zip(X.columns,clf_up.coef_[0])), key = lambda x: x[1],reverse=True) 


# ## Train a random forest model

# In[15]:


from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(random_state=0).fit(X_train, y_train)


# In[16]:


predictions_rfc = rfc.predict(X_test)
# print(classification_report(y_test,predictions_rfc))


# In[17]:


roc_auc(rfc,'rfc', X_test, y_test)


# In[18]:


sorted(list(zip(X.columns,rfc.feature_importances_)), key = lambda x: x[1],reverse=True) 


# In[19]:


# Not bad. Save
pickle.dump(rfc, open(os. getcwd()[:-9] +'Model/rfc_HW.pkl', 'wb'))

