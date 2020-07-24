# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 
DATA_URL = ("Data.xlsx")
data = pd.read_excel('Data.xlsx')
data = data[0:2000]

####
st.title("Data Analytics - Willow Park Golf Course - Restaurant Data - June 20 2020 to July 20 2020")
st.markdown("This is a streamlit dashboard used to analyze data and provide data-driven solutions to business optimization Problem. Analyzing the data from the first month of business post COVID-19 lockdown will help take actions that will result in improved business performance. 🗽💥")
if st.checkbox("Show Data", False):
    st.subheader('Data')
    st.write(data)
####

####
df2 = data[['Order_ID', 'SERVER','TOTAL']]
group = df2.groupby('Order_ID')
df3 = group['TOTAL'].agg([np.sum])
df4 = df2[['Order_ID','SERVER']]
df4 = df4.drop_duplicates()
group2 = df2.groupby('SERVER')
df5 = group2['TOTAL'].agg([np.sum])
df5['SERVER_NAME'] = df5.index
df6 = df4['SERVER'].value_counts()
df6.columns = ['server_name','num_of_bills']
df6 = df6.to_frame()
df6['SERVER_NAME']=df6.index
df7 = pd.merge(df5, df6, on='SERVER_NAME', how='outer')
df7['avg_bill'] = df7['sum']/df7['SERVER']
df7 = df7.rename(columns={"sum": "Total revenue generated", "SERVER_NAME": "Server Name", "SERVER" : "Customers served", "avg_bill" : "Average revenue per bill"})
df7.sort_values(by='Average revenue per bill', ascending=False)
q = df7.sort_values(by='Average revenue per bill', ascending=False)
w = df7.sort_values(by='Total revenue generated', ascending = False)
df8 = df7
df9 = data[['DATE','TOTAL']]
a = df9.groupby('DATE')
df9 = a['TOTAL'].agg([np.sum])
df10 = data[['DATE','Order_ID']]
b = df10.groupby('DATE')
df10 = b['Order_ID'].nunique()
df11 = pd.merge(df9, df10, on='DATE', how='outer')
df11['avg'] = df11['sum']/df11['Order_ID']
df11.std()

st.header("Server performances for the month :")
select = st.selectbox('Show the list of servers by:', ['Efficiency', 'Revenue generated', 'Customers attended'])

if select == 'Efficiency':
        st.write(q)
        st.markdown("Standard deviation for average revenue generated everyday is %i dollars" %(df11['avg'].std()))
        st.markdown("The standard deviation in the average revenue generated by the servers is %i. (Ignoring outlier server name Bailey T.) The total number of customers served by the server's with low average revenue generated is %i. (Contributing to negative standard deviation.) Replacing these servers with the server's with higher average revenue or awarding performance based incentives will see an improved business as follows : %i * %i = $ %i i.e. %i percent increase in revenue." %(df11['avg'].std(), df8['Customers served'][8:].sum() , df11['avg'].std(),  df8['Customers served'][8:].sum() , df11['avg'].std() * df8['Customers served'][8:].sum() , ((df11['avg'].std() *df8['Customers served'][8:].sum())/df11['sum'].sum())*100))
if select == 'Revenue generated':
        st.write(df7.sort_values(by='Total revenue generated', ascending=False))
        st.markdown("Deb, Jillian and Ashley have attended %i of the total %i customers in the month, contributing to more than half of the revenue generated. Jillian has a higher average revenue per bill" %(w['Customers served'][0:3].sum() , w['Customers served'].sum()))
elif select == 'Customers attended':
        st.write(df7.sort_values(by='Customers served', ascending=False))
        
        
###
d12 = data[[ 'DATE','DAY','TOTAL','WEEK NUMBER']]
def top(g):
    return g['DAY'].value_counts().idxmax()
topdf = d12.groupby('DATE').apply(top)
topdf = topdf.to_frame()
topdf.columns = ['DAY']
d13 = topdf['DAY'].value_counts()
d13 = d13.to_frame()
d13.index.names = ['DAY']
d13.columns = ['DAYS']
group4 = d12.groupby('DAY')
d14 = group4['TOTAL'].agg([np.sum])
e = pd.merge(d14, d13, on='DAY', how='outer')
e['Average day of week'] = e['sum']/e['DAYS']
e = e.loc[['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'], :]
e.columns = ['Total revenue for this day', 'Number of working days', 'Average revenue']
a1 = (e['Average revenue'][1] + e['Average revenue'][3] + e['Average revenue'][4:].sum())/5
a2 = (e['Average revenue'][0] + e['Average revenue'][2])/2 
a3 = a1 - a2
a4 = data['TOTAL'].sum()
a5 = ((a3 * 4) / (data['TOTAL'].sum())) * 100

st.header("Best days to keep the restaurant closed for maintenance and sanitization :")
Day = e.index 
Average = e['Average revenue'] 
  
# Figure Size 
fig, ax = plt.subplots(figsize =(16, 9)) 
  
# Horizontal Bar Plot 
ax.barh(Day, Average) 
  
# Remove axes splines 
for s in ['top', 'bottom', 'left', 'right']: 
    ax.spines[s].set_visible(False) 
  
# Remove x, y Ticks 
ax.xaxis.set_ticks_position('none') 
ax.yaxis.set_ticks_position('none') 
  
# Add padding between axes and labels 
ax.xaxis.set_tick_params(pad = 5) 
ax.yaxis.set_tick_params(pad = 10) 
  
# Add x, y gridlines 
ax.grid(b = True, color ='grey', 
        linestyle ='-.', linewidth = 0.5, 
        alpha = 0.2) 
  
# Show top values  
ax.invert_yaxis() 
  
# Add annotation to bars 
for i in ax.patches: 
    plt.text(i.get_width()+0.2, i.get_y()+0.5,  
             str(round((i.get_width()), 2)), 
             fontsize = 10, fontweight ='bold', 
             color ='grey') 
  
# Add Plot Title 
ax.set_title('Average revenue by days of the week', 
             loc ='left', ) 
  
# Add Text watermark 
fig.text(0.9, 0.15, 'Rohit Bhalerao', fontsize = 12, 
         color ='grey', ha ='right', va ='bottom', 
         alpha = 0.7) 
  
# Show Plot 
plt.show() 
st.write(fig)

st.write(e) 
st.markdown("Even though Tuesdays and Thursdays see a good business than other days of the week, the restaurant was closed on 2 Tuesdays and 3 Thursdays in the 5 weeks. So, it is suggested to change this, and to keep the restaurant closed on either Monday's or Wednesday's for Sanitization and Maintenance purpose. The average business of Tuesdays, Thursdays, Fridays and the weekends is %i $. The average business of Wednesdays and Mondays is %i $.This action will add up the revenue by around %i $ every week, i.e. , %i $ a month. Business performance will improve by around %i percent." %(a1, a2 , a3 , a3 * 4 , a5))
