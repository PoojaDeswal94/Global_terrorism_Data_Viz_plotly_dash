#!/usr/bin/env python
# coding: utf-8

# # Data Visualization Final Project
# 
# 
# *Pooja DESWAL*
# 
# *Levon AVETISYAN*
# 
# *Jyothish Kumar CHANDRASENAN GEETHAKUMARI*
# 
# **Msc Data Science & Analytics**
# 
# **Fall 2019- 2021**

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px


# In[2]:


data = pd.read_csv('globalterrorismdb.csv',encoding= 'ISO-8859-1')
print(data.info())
print(data.shape)


# In[3]:


data.columns.values


# In[4]:


data.rename(columns = {'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
terrorism_data = data[['Year','Month','Day','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
terrorism_data['casualities'] = data['Killed'] + data['Wounded']
terrorism_data.head(20)


# In[5]:


print(terrorism_data.info())
print(terrorism_data.shape)


# In[6]:


fig1 = px.histogram(terrorism_data, x="Year",nbins=25,title='Frequency of Terrorism Activities by Years',width=1500, height=800)
#fig1.show()


# # Inference 
# 
# *More Terrorist Activities reported during* **2012-2017**
# 
# 

# In[7]:


#Analysis of casualities around the globe between 1970-2011.

world_terrorism = terrorism_data.groupby(['Year', 'Country'])['casualities'].max().reset_index()
fig2 = px.choropleth(world_terrorism, locations="Country", locationmode='country names', 
                     color="casualities", hover_name="Country",hover_data = [world_terrorism.casualities],projection="mercator",
                     animation_frame="Year",width=1600, height=1000,
                     color_continuous_scale='reds',
                     range_color=[0,10000],

                     title='Analysis of casualities around the globe between 1970-2011')

fig2.update(layout_coloraxis_showscale=True)
fig2.update_layout(
    autosize=False,
    width=1800,
    height=1000)


# # Inference 
# 
# *Maximum casuality* 
# **Country : USA ; 
#   Year: 2001 ; 
#   Casualities: 9574**

# In[8]:


fig3 = px.density_heatmap(terrorism_data, x="Year", y="AttackType",title="Attack Type of Terrorists from 1970 - 2017", color_continuous_scale='RdBu_r',width=1500, height=800)
#fig3.show()


# In[9]:


region_data = pd.value_counts(terrorism_data['Region'])
print(region_data.index)
fig4 = px.pie(region_data, values= region_data.values, names = region_data.index,
              title='Terrorist Activities Reported By Region',hole=.3,width=1500, height=800)
#fig2.update_traces(textposition='inside', textinfo='percent+label')
#fig4.show()


# # Inference 
# 
# *Maximum Terrorist Activities reported in Region* **Middle East and North Africa**
# 
# *Least Terrorist Activities reported in Region* **Australasia and Oceania**

# In[10]:


Terrorism_Middle_East = terrorism_data[terrorism_data.Region == 'Middle East & North Africa']
#Terrorism_Middle_East

ME_data = pd.value_counts(Terrorism_Middle_East['Country']).sort_values(ascending=False).iloc[0:10]
print(ME_data.index)
fig5 = px.bar(ME_data, x= ME_data.values, y = ME_data.index,
              title='Countries mostly affected by Terrorist Activities in Middle East and North Africa', orientation='h',width=1500, height=800)
#fig2.update_traces(textposition='inside', textinfo='percent+label')
fig5.update_traces(marker_color='darkred')
#fig5.show()


# # Inference 
# 
# *Maximum Terrorist Activities reported in Region* **Middle East and North Africa** *for country* **Iraq**
# 
# 

# In[11]:


Terrorism_Australasia_Oceania = terrorism_data[terrorism_data.Region == 'Australasia & Oceania']
#Terrorism_Middle_East

AO_data = pd.value_counts(Terrorism_Australasia_Oceania['Country']).sort_values(ascending=False).iloc[:10]
print(AO_data.index)
fig6 = px.bar(AO_data, y= AO_data.values, x = AO_data.index,
              title='Countries leastly affected by Terrorist Activities in Australasia & Oceania ',width=1500, height=800)
#fig2.update_traces(textposition='inside', textinfo='percent+label')
fig6.update_traces(marker_color='darkgreen')
#fig6.show()


# # Inference 
# 
# *Maximum Terrorist Activities reported in Region* **Australasia & Oceania** *for Island* **New Hebrides**
# 
# 

# In[12]:


fig7 = px.treemap(Terrorism_Middle_East, path=[ 'Region', 'Target_type' ], values='casualities',title='Terrorists Targeted Type in Middle East & North Africa',width=1500, height=800)
#fig7.show()


# In[13]:


terrorism_max = terrorism_data[(terrorism_data['Group'] != 'Unknown') & (terrorism_data['casualities'] > 50)]
#terrorism_max.head()
terrorism_max = terrorism_max.sort_values(['Region', 'Country'])
terrorism_max.head()


# In[14]:


hover_text = []
for index, row in terrorism_max.iterrows():
    hover_text.append(('city: {city}<br>'+
                      'Group: {group}<br>'+
                      'casualities: {casualities}<br>'+
                      'Year: {year}').format(city=row['city'],
                                            group=row['Group'],
                                            casualities=row['casualities'],
                                            year=row['Year']))
terrorism_max['text'] = hover_text


# In[15]:


trace0 = go.Scatter(
    x=terrorism_max['Year'][terrorism_max['Country'] == 'Iraq'],
    y=terrorism_max['casualities'][terrorism_max['Country'] == 'Iraq'],
    mode='markers',
    name='Iraq',
    text=terrorism_max['text'][terrorism_max['Country'] == 'Iraq'],
    marker=dict(
        symbol='circle',
        sizemode='area',
        size=terrorism_max['casualities'][terrorism_max['Country'] == 'Iraq'],
        line=dict(
            width=2
        ),
    )
)

trace1 = go.Scatter(
    x=terrorism_max['Year'][terrorism_max['Country'] == 'Turkey'],
    y=terrorism_max['casualities'][terrorism_max['Country'] == 'Turkey'],
    mode='markers',
    name='Turkey',
    text=terrorism_max['text'][terrorism_max['Country'] == 'Turkey'],
    marker=dict(
        symbol='circle',
        sizemode='area',
        size=terrorism_max['casualities'][terrorism_max['Country'] == 'Turkey'],
        line=dict(
            width=2
        ),
    )
)


trace2= go.Scatter(
    x=terrorism_max['Year'][terrorism_max['Country'] == 'Algeria'],
    y=terrorism_max['casualities'][terrorism_max['Country'] == 'Algeria'],
    mode='markers',
    name='Algeria',
    text=terrorism_max['text'][terrorism_max['Country'] == 'Algeria'],
    marker=dict(
        symbol='circle',
        sizemode='area',
        size=terrorism_max['casualities'][terrorism_max['Country'] == 'Algeria'],
        line=dict(
            width=2
        ),
    )
)

layout1 = go.Layout(
         title = 'Comparision of Terrorism between Iraq,Turkey and Algeria',
         width=1500, height=800,
         xaxis = dict(
             title = 'Year',
             #type = 'log',
             range = [1970,2017],
             tickmode = 'auto',
             nticks = 40,
             showline = True,
             showgrid = False
             ),
         yaxis = dict(
             title = 'Casualities',
             type = 'log',
             range = [1.5,4],
             tickmode = 'auto',
             nticks = 50,
             showline = True,
             showgrid = False),
         paper_bgcolor='rgb(243, 243, 243)',
         plot_bgcolor='rgb(243, 243, 243)',
         )


data1 = [trace0, trace1,trace2]

fig8 = go.Figure(data=data1, layout=layout1)
#fig8.show()


# # Inference 
# 
# **Comparision of Terrorism between Iraq,Iran and Algeria** 
# *Between 1970 - 2001 Algeria had more terror attacks when compared to Iraq and Turkey, whereas between 2002-2016 Iraq has most number of terror activities followed by Algeria and Turkey .*

# In[16]:


text = "Work is prepared by\nPooja DESWAL\nLevon AVETISYAN\nJyothish Kumar CHANDRASENAN GEETHAKUMARI\n\nMsc Data Science & Analytics\nFall 2019-2021\n\nWe choose to analyze the terrorist activity as we consider this problem one of the biggest challenges for modern society. Even if casualties from terrorist attacks may seem not big, we think that social and mental impact is huge. We understand that our small research will not add big value but we think that any research in this field is valuable.\n\nWe used data from the kaggle.com https://www.kaggle.com/START-UMD/gtd"




# In[17]:


import dash
import dash_core_components as dcc
import dash_html_components as html

Terrorism_Analysis = dash.Dash()
Terrorism_Analysis.layout = html.Div([html.Div([html.H1("Data Visualization Final Project"),html.P("World wide analysis of Terrorism from 1970 - 2017")],
                                        style = {'width': '100%','padding' : '50px' ,'backgroundColor' : '#3EB7EE','font-family': "sans serif", 'color' :'white','font-size':'300%'}),
                                dcc.Textarea(
        id='start_text',value=text,style={'width': '100%', 'height':250,'padding' : '50px' ,'font-family': "sans serif", 'color' :'marron','font-size':'150%'}),
        html.Div(id='start_text_output', style={'whiteSpace': 'pre-line'}),
                                 dcc.Graph(figure=fig1),                             
                                 dcc.Graph(figure=fig2),                        
                                 dcc.Graph(figure=fig3),
                                 dcc.Graph(figure=fig4),
                                 dcc.Graph(figure=fig5),
                                 dcc.Graph(figure=fig6),
                                 dcc.Graph(figure=fig7),
                                 dcc.Graph(figure=fig8)
                                     ])


Terrorism_Analysis.run_server(debug=True, use_reloader=False)


# In[ ]:




