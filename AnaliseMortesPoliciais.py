#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from jupyterthemes import jtplot
jtplot.style(theme='monokai')
df = pd.read_csv(r'C:\Users\MASTER\Desktop\kaggle\police_deaths_in_america_v2.csv', sep=',')
df = df.drop(['Date', 'K9_Unit', 'Name'], axis='columns')
display(df)
df.info()


# ## Causa de mortes tem a maior parte causada por tiros 
# * 50% das mortes são causadsa por tiros
# * Nas demais mortes as maiorias  são causadas por acidentes

# In[2]:


for morte, quantidade in df['Cause_of_Death'].value_counts().items():
    if quantidade < 500:
        df.loc[df['Cause_of_Death'] == morte, 'Cause_of_Death']= 'Outros'
print(df['Cause_of_Death'].value_counts())


# In[19]:


plt.figure(figsize=(25,7))
sns.countplot(x='Cause_of_Death', data=df, order = df['Cause_of_Death'].value_counts().index)


# ## Cidade e Departamentos
# - As mortes estão repartidas em todos os estados por tanto todas elas serão encaixadas como ''Outros'' já que o objetivo da analise não é em estados especificas só apenas as que tem os maiores mortes contabilizadas 
# - No top 5 temos : 1- Texas com 2230 mortes, 2- United States com 1970 mortes, 3- New york com 1880 mortes, 4- California com 1784 mortes e 5- Illinis com 1174 mortes.
# - No Texas as mortes contabilizadas estão em varios departamentos porém o Texas Rangers, Houston police department e Texas Department of Criminal Justice - Correctional Institutions Division 
# - No departamento Texas Rangers as patentes dos policias mortos estão privadas | No departamento Houston Police Department as patentes dos policias mortos na sua maioria são ''Police Oficcer'', "Oficcer" e "Detective".
# - No United States em segundo lugar com mais mortes registradas os departamentos com mais mortes registradas são United States Marshals Service, United States Customs Service e Federal Bureau of Investigation
# - No departamento United States Marshals Service a patente com mais mortes registradas são de "Deputy U.S. Marshal" e "Special Deputy Marshal "
# - Optei por priorizar apenas por 3 estados para saber a patente dos policiais vulneraveis nos departamentos
# 

# In[35]:


for estado, quantidade in df['State'].value_counts().items():
    if quantidade < 600:
        df.loc[df['State'] == estado, 'State']= 'Outros'
print(df['State'].value_counts())


# In[21]:


df_splt = df['Department'].str.split(',',n = 1, expand = True)
df['Departamento'] = df_splt[0]
df = df.drop('Department', axis='columns')
display(df)


# In[41]:


df_texas = df.loc[df['State'] == 'Texas']
df_department = df_texas.loc[df['Departamento'] == 'Houston Police Department']
for departamento, quantidade in df_texas['Departamento'].value_counts().items():
    if quantidade < 70:
        df_texas.loc[df_texas['Departamento'] == departamento, 'Departamento'] = 'Outros'
print(df_texas['Departamento'].value_counts())
print(df_department['Rank'].value_counts())
display(df_department)


# In[46]:


df_us = df.loc[df['State'] == 'United States']
df_department_us = df_us.loc[df['Departamento'] == 'United States Department of Justice - United States Marshals Service']
print(df_us['Departamento'].value_counts())
print(df_department_us['Rank'].value_counts())


# ## A patente dos policiais mortos em sua maioria eram diversas e estão descrevidas como ''outros''  porém os Patrolman, Police Oficer e Deputy Sheriff  foram que tiveram mais baixa

# In[9]:


for rank, quantidade in df['Rank'].value_counts().items():
    if quantidade < 500:
        df.loc[df['Rank'] == rank, 'Rank'] = 'Outros'
print(df['Rank'].value_counts())


# In[10]:


plt.figure(figsize=(25,7))
sns.countplot(x='Rank', data=df, order = df['Rank'].value_counts().index)


# 
# ## Grafico representando as quantidade de mortes anuais ao longo dos anos

# In[4]:


print(df['Year'].value_counts())


# In[141]:


grupo_ano = df.groupby('Year')['Rank'].count()
plt.figure(figsize=(20,7))
sns.lineplot(x=grupo_ano.index, y=grupo_ano.values, data = grupo_ano, linewidth = 2.5, color = '#626567')
plt.xticks(range(1800,2022, 10), fontsize = 15)
plt.title('Grafico de quantidade de mortes anuais', fontsize = 18)
plt.xlabel('Ano')
plt.ylabel('Quantidade')

plt.show()


# ## Decidi pegar nessa ultima etapa o ano de 2021 completo para fazer analise 
# - A principal causa das mortes em 2021 foi o covid 19 representando %68.89 das mortes em geral
# -
# - Dezembro, Agosto e Janeiro estão no top 3 de quantidade de mortes no ano. ( Setembro = 114 mortes , Agosto = 108 mortes, Janeiro = 72 )
# -
# - Dos 3 meses liderados em 2021 o covid pricipal motivo sendo respresentado da seguinte forma:  Setembro teve %90,35 de mortes por covid das 114 mortes |  Agosto teve %82.40 de mortes por covid das 108 mortes | Janeiro teve %73.61 de mortes por covid das 72 mortes
# -
# - Texas, Florida, US e Georgia foram os estados com mais mortes registradas e com os indices maiores de covid 
# 1 - Texas teve 110 mortes em 2021 e o Covid foi responsavel por %86.36 das mortes
# 2 - Florida teve 60 mortes em 2021 e o Covid foi responsavel por %81.66 das mortes
# 3 - US teve 58 mortes em 2021 e o Covid foi responsavel por %72.41 das mortes
# 4 - Georgia teve 53 mortes em 2021 e o Covid foi responsavel por %75.47 das mortes 
# ### Detalhes dessa etapa 
# - Criei um novo df apenas com as mortes causada pelo covid e apartir daí fiz as comparações e tive os resultados esperados entendendo o motivo principal das mortes

# In[198]:


df_2021 = df.loc[df['Year'] == 2021]
df_2021 = df_2021.drop('Department', axis='columns')
#
#
df_2021['Month'].value_counts()
df_2021['Cause_of_Death'].value_counts()
df_2021['Day'].value_counts()
df_2021['Department'].value_counts()
df_2021['State'].value_counts()


# In[199]:


df_2021_covid = df_2021.loc[df['Cause_of_Death'] == 'COVID19']
df_2021_covid['State'].value_counts()
display(dd)


# ## Conclusão
# * Nesse projeto a base de dados utilizada foi do Kaggle, um registro de mortes de policiais de 1791 até 2022, nesse projeto fiz uma analise de dados buscando trazer a utilização de Graficos com matplotlib e seaborn, o projeto de analise foi explorar os dados disponiveis e conseguir detalhadamente saber alguns topicos como :
# 1 - Principais Causas de mortes de policiais
# 2 - Principais cidades e departamentos com mais mortes registradas
# 3 - Patentes com mais mortes 
# 4 - Representatividade em grafico de mortes ao longo dos anos 
# 5 - Impacto da covid na base de dados
# * Um dos pilares mais importantes que consegui tirar da Base de dados foi o impacto da covid, as mortes ao longo de todos os anos foram aumentando gradativamente porém 2020 e 2021 deu um salto alarmante onde desde 1930 nunca teve tantas baixas em um ano. Para se ter de comparativo em 1930 foram registradas 347 mortes no total e em 2020 quase 70 anos depois 436 baixas sendo elas a grande maioria pelo covid e em 2021 conseguiu quase dobrar as baixas com 643 baixas.
# * Como 2021 teve muitas baixas registradas usei ele como alvo parar tirar os meses com mais mortes, departamentos e cidades.

# In[ ]:




