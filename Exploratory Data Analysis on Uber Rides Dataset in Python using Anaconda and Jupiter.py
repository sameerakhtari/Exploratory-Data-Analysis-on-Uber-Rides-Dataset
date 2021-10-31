#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Data Discovery

# Libraries for handling numeric computation and dataframes
import pandas as pd
import numpy as np

# Libraries for statistical plotting
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# My personal data storaged in my Github repository
rides = pd.read_csv('https://raw.githubusercontent.com/sameerakhtari/Exploratory-Data-Analysis-on-Uber-Rides-Dataset/main/raw-data/My%20Uber%20Drives%20-%202016.csv')


# In[2]:


rides.info()


# In[3]:


rides.rename(columns={'START_DATE*': 'start_date', 'END_DATE*': 'end_date','CATEGORY*':'category','START*':'start',
                      'STOP*':'stop','MILES*':'miles','PURPOSE*':'purpose'}, inplace=True)


# In[4]:


rides.head()


# In[5]:


#creating an additional dataframe without Uber EATS records (out of analysis scope)
df1 = rides[rides.category!='UberEATS Marketplace'][['miles']]

print(df1.describe().transpose().round(1));
df1.boxplot(grid=False);


# In[ ]:


#Data Preparation


# In[6]:


rides.isnull().sum().sort_values(ascending=False)


# In[7]:


rides[rides.category.isnull()]


# In[8]:


rides.dropna(subset = ['category'], inplace=True)


# In[9]:


rides[rides.category.isnull()]


# In[10]:


rides[rides.end_date.isnull()]


# In[11]:


rides.isnull().sum().sort_values(ascending=False)


# In[12]:


rides[rides.start.isnull()]


# In[13]:


rides.dropna(subset = ['start'], inplace=True)


# In[14]:


rides.dropna(subset = ['stop'], inplace=True)


# In[15]:


rides.isnull().sum().sort_values(ascending=False)


# In[16]:


# Checking categories in product_type column
print(rides.purpose.value_counts())


# In[17]:


# Library for manipulating dates and times
from datetime import datetime
from datetime import timedelta

# Function to convert features to datetime
def date_convertion(df, cols):

  for col in cols:
    df[col] = df[col].apply(lambda x: x.replace(' +0000 UTC', ''))
    df[col] = pd.to_datetime(df[col])
    
  return df

# Applying date_convertion function to date features 
rides = date_convertion(rides, ['start_date', 'end_date'])


# In[18]:


rides['month'] = rides.start_date.map(lambda x: datetime.strftime(x,"%b"))


# In[19]:


rides['weekday'] = rides.start_date.map(lambda x: datetime.strftime(x,"%a"))


# In[20]:


rides['year'] = rides.start_date.map(lambda x: datetime.strftime(x,"%Y"))


# In[21]:


rides['time'] = rides.start_date.map(lambda x: datetime.strftime(x,"%H:%M"))


# In[22]:


rides['month'] = rides.end_date.map(lambda x: datetime.strftime(x,"%b"))


# In[23]:


rides['weekday'] = rides.end_date.map(lambda x: datetime.strftime(x,"%a"))


# In[24]:


rides['year'] = rides.end_date.map(lambda x: datetime.strftime(x,"%Y"))


# In[25]:


rides['time'] = rides.end_date.map(lambda x: datetime.strftime(x,"%H:%M"))


# In[26]:


#Now Finding ride time 
rides['request_lead_time'] = rides.end_date - rides.start_date
rides['request_lead_time'] = rides['request_lead_time'].apply(lambda x: round(x.total_seconds()/60,1))


# In[28]:


#Data Analysis Time


# In[29]:


#listing completed rides
completed_rides = rides[(rides.end_date!='')] 


# In[30]:


#A). How many trips I did over the years?
print('Total trips: ', completed_rides.end_date.count())
print(completed_rides.year.value_counts().sort_index(ascending=True))
sns.countplot(data=completed_rides, x='year',order=['2014','2015','2016','2017','2018','2019'], palette='pastel');


# In[31]:


#B). How many trips were Completed on what Purpose?
print('Total trips: ', rides.end_date.count())
print(round(rides.end_date.value_counts()/rides.end_date.size*100,1))

sns.countplot(data=rides, x='year', order=['2016'], hue='purpose', palette='coolwarm');
rides.groupby(by=['year'])['purpose'].value_counts(normalize=True).unstack('year').plot.bar(stacked=True);


# In[43]:


#C). For What reason Went to what place...?!?




rides.groupby(by=['stop'])['purpose'].value_counts(normalize=True).unstack('stop').plot.bar(stacked=True);

