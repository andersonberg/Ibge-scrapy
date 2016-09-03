
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[2]:

ans = pd.read_excel("Planilhas/ANS Vidas Assistidas.xls", sheetname="Sudeste")
ans.head()


# In[4]:

equipamentos = pd.read_excel("Planilhas/Equipamentos por município Sudeste.xls")


# In[5]:

def get_equipment(equip):
    raio_x = equip[equip["equipamento"].map(lambda x: "raio x" in x.encode('utf8').lower() and "dentario" not in x.encode('utf8').lower() and "densitometria" not in x.encode('utf8').lower() )]
    mamografo = equip[equip["equipamento"].map(lambda x: "mamografo" in x.encode('utf8').lower() )]
    ultrassom = equip[equip["equipamento"].map(lambda x: "ultrassom" in x.encode('utf8').lower() )]
    ressonancia = equip[equip["equipamento"].map(lambda x: "ressonancia" in x.encode('utf8').lower() )]
    tomografo = equip[equip["equipamento"].map(lambda x: "tomógrafo" in x.encode('utf8').lower() )]
    pet_ct = equip[equip["equipamento"].map(lambda x: "pet/ct" in x.encode('utf8').lower() )]
    gama = equip[equip["equipamento"].map(lambda x: "gama" in x.encode('utf8').lower() )]
    
    total_sum = {"XP":0, "US": 0, "MR":0, "CT":0, "MI":0}
    
    if not raio_x.empty:
        total_sum.update({"XP": raio_x["existentes"].sum() + mamografo["existentes"].sum()})
    if not ultrassom.empty:
        total_sum.update({"US": ultrassom["existentes"].sum()})
    if not ressonancia.empty:
        total_sum.update({"MR": ressonancia["existentes"].sum()})
    if not tomografo.empty:
        total_sum.update({"CT": tomografo["existentes"].sum()})
    if not pet_ct.empty:
        total_sum.update({"MI": pet_ct["existentes"].sum() + gama["existentes"].sum()})
    
    return total_sum


# In[16]:

populacao = pd.read_excel("Planilhas/Sudeste/total_populacao_sao_paulo.xls")
print(populacao.shape)
populacao.head()


# In[17]:

pib = pd.read_excel("Planilhas/PIBMunicipal2008-2012.xlsx", header=5, parse_cols="A,F,G")
# Ajustar o slide para o Estado sendo processado
pib = pib[3290:3935]
pib


# In[18]:

columns = [u"Município", u"Produto Interno Bruto (R$ 1.000 )", u"PIB per capita (R$)", u"Quantidade (Pessoas)", "Vidas Assistidas ANS", "XP", "US", "MR", "CT", "MI"]
result_final = pd.DataFrame(columns=columns)

city_list=[]
for row in populacao.iterrows():
    try:
        city_code = int(row[1][u"Código do município"][:-1])
        city_pop = int(row[1][u"Total da população 2010"])
        city_name = row[1][u"Nome do município"]
        
        # Obtém a quantidade de vidas assistidas
        result2 = ans[ans[u"Município"].map(lambda x: str(city_code) in x)]
        
        if result2.empty:
            city_assist = 0
        else:        
            city_assist = int(result2[u"Assistência Médica"])
        
        # Obtém PIB e PIB per capita
        result3 = pib[pib[u"Município"]==city_name]
        
        if result3.empty:
            city_pib = 0
            city_pib_per_capita = 0 
        else:
            city_pib = float(result3[2012])        
            city_pib_per_capita = float(result3[u"Per capita (R$) 2012"])
            
        info_dict = {u"Município":city_name, u"Produto Interno Bruto (R$ 1.000 )":city_pib, u"PIB per capita (R$)":city_pib_per_capita, u"Quantidade (Pessoas)":city_pop, "Vidas Assistidas ANS":city_assist}
            
        # Obtém a quantidade de máquinas por categoria
        equip = equipamentos[equipamentos["cidade"]==city_code]
        total_sum = get_equipment(equip)
        
        info_dict.update(total_sum)
        city_list.append(info_dict)

    except ValueError:
        print 'ValueError'
        continue
    except TypeError:
        print 'TypeError'
        print result3.head()
        print city_name
        continue

result_final = result_final.append(city_list, ignore_index=True)

# Trocar o nome da planilha para o Estado sendo processado
result_final.to_excel("Cobertura SP.xls")


# In[103]:

curr_city = int(populacao[u"Código do município"][10][:-1])
curr_city_population = populacao[u"Total da população 2010"][10]
curr_city_name = populacao[u"Nome do município"][10]
equip = equipamentos[equipamentos["cidade"]==curr_city]

raio_x = equip[equip["equipamento"].map(lambda x: "raio x" in x.encode('utf8').lower() )]
ultrassom = equip[equip["equipamento"].map(lambda x: "ultrassom" in x.encode('utf8').lower() )]
ressonancia = equip[equip["equipamento"].map(lambda x: "ressonancia" in x.encode('utf8').lower() )]
tomografo = equip[equip["equipamento"].map(lambda x: "tomógrafo" in x.encode('utf8').lower() )]
pet_ct = equip[equip["equipamento"].map(lambda x: "pet/ct" in x.encode('utf8').lower() )]

total_sum = {}
total_sum.update({"XP": raio_x["existentes"].sum()})
total_sum.update({"US": ultrassom["existentes"].sum()})
total_sum.update({"MR": ressonancia["existentes"].sum()})
total_sum.update({"CT": tomografo["existentes"].sum()})
total_sum.update({"MI": pet_ct["existentes"].sum()})

print total_sum

sum_xp = raio_x[["existentes"]].sum()
sum_us = ultrassom[["existentes"]].sum().append(sum_xp)
sum_mr = ressonancia[["existentes"]].sum().append(sum_us)
sum_ct = tomografo[["existentes"]].sum().append(sum_mr)
sum_mi = pet_ct[["existentes"]].sum().append(sum_ct)

# df_sum = pd.DataFrame(data=sum_mi, columns=["XP", "US", "MR", "CT", "MI"])
# df_sum = df_sum.append(sum_us, ignore_index=True)
# pd.merge(df_sum, sum_ultrassom)
# df_sum = df_sum.append(sum_ultrassom, ignore_index=True)
# df_sum
# sum_mi


# In[120]:

result3 = pib[pib[u"Município"]==curr_city_name]
result3


# In[129]:

city_pib = float(result3[2012])
city_pib_per_capita = float(result3[u"Per capita (R$) 2012"])
city_assist = int(result2[u"Assistência_Médica"])
city_pib, city_assist


# In[139]:

dict_result = {u"Município":curr_city_name, u"Produto Interno Bruto (R$ 1.000 )":city_pib, u"PIB per capita (R$)": city_pib_per_capita, u"Quantidade (Pessoas)":curr_city_population, "Vidas Assistidas ANS":city_assist}
columns = dict_result.keys()
result_final = pd.DataFrame(data=dict_result, index=["Município"])
pd.pivot_table(result_final, index=[u"Município"])


# In[ ]:



