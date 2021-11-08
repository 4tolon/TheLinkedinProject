#!/usr/bin/env python
# coding: utf-8

import requests 
import json
import os
from dotenv import load_dotenv
import pandas as pd
from pandas import json_normalize
from bs4 import BeautifulSoup 
import time
from random import randint


load_dotenv()
linkedin = os.getenv("link")


params = {'oauth2_access_token': linkedin}
response = requests.get('https://api.linkedin.com/v2/me', params = params)
print(json.dumps(response.json(), indent=1))
response

datos = response.json()
data = pd.read_csv('../data/Connections.csv', skiprows=2)
data.head()
data.info()


def capastrings(x):
    """ 
    Funcion para limitar la informacion de los String a la mitad.
    argg = string
    """
    s = len(x)//2 
    return x[:s]

data["Name"] = data["First Name"].astype(dtype=str).apply(capastrings)
data["Lname"] = data["Last Name"].astype(dtype=str).apply(capastrings)


data = data.drop(['First Name', 'Last Name', 'Email Address'], axis = 1)

nombres_emp = list(data.Company)
print(type(nombres_emp))
nombres_emp = [str(nom).replace(" ", "+") for  nom in nombres_emp]
data['nomb_busc'] = nombres_emp
# Lista de resultados a buscar 
data['urls'] = ['https://www.axesor.es/buscar/empresas?q='+comp+'#resultados' for comp in nombres_emp] 
data


def sopera(url):
    '''
    Funcion para scaperara la web de axesor, se aplica a una columna del data frame con un determinado formato y crea una columna nueva con la direccion web de los resultados de la Busqueda, en este caso concreto el resultado es el enlace de la web de la empresa que  aparece primero en los resultados de la busquedaself.

    '''
    t=0
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        tabla = soup.findAll('table')
        elemento = tabla[0].find_all('a')[0]
        suburl = 'https:'+elemento['href']
        time.sleep(0.5)
        print(f'Rico Rico!{t}')
        t+=1
        return suburl
    except:
        return 'error'

data["suburl"] = data.urls.apply(sopera)
#data_primer_scra = data.to_csv('../data/data_primer_scra2.csv')


df = pd.read_csv('../data/data_primer_scra.csv')
list_of_dfs = [df.loc[i:i+10-1,:] for i in range(0, len(df),10)]




list_of_dfs[0]


len(list_of_dfs)

def avecrema(suburl):
    '''
    Super funcion para enriquezer el dafaframe, se aplica en la colunna de df generada con la anterior funcion "sopera", y realiza una requests a esa direcion,self.mediante parseo y sopeo limpia el resultado generando un dicionario e introduciendolo en una nueva columna. Ese dicionario esta compuesto por  los valoles de los datos que ofrece la web de manera gratuita. 

    !!!!!! Pero me han pillado con tantas peticiones a la web y solo me permiten las diez primera peticiones, he intentado de todo, he puesto tiempos de espera entre peticion y peticion pero no ha habido manera, he dividido el data frame de mis contactos en una lista de 78 df de diez filas para ir haciendolo poco a poco. pero asi tampoco me ha salido. !!!!!


    '''
    t= 0
    try:
        dic_emp = {}
        loop=0
        r = requests.get(suburl)
        subsoup = BeautifulSoup(r.content,"html.parser")
        subtabla = subsoup.findAll('table')
        for i in range(9):
            subelemento = subtabla[0].find_all('tr')[i]
            t = subelemento.text
            tt = t.split(sep=':', maxsplit=-1)    
            dic_emp.update({tt[0]:tt[1]}) 
        #time.sleep(randint(2, 5))
        print(f'Rico Rico y enriquecido!  {loop}')
        loop += 1
        return dic_emp
    except:
        try:
            dic_emp = {}
            r = requests.get(suburl)
            subsoup = BeautifulSoup(r.content,"html.parser")
            subtabla = subsoup.findAll('table')
            itera = len(subtabla[0].find_all('tr'))
            for i in range(itera):
                subelemento = subtabla[0].find_all('tr')[i]
                t = subelemento.text
                tt = t.split(sep=':', maxsplit=-1)    
                dic_emp.update({tt[0]:tt[1]}) 
            #time.sleep(randint(2, 5))
            print(f'Rico Rico y enriquecido!  {loop}')
            loop += 1
            return dic_emp
        except:
            print('Error')
            return 'error'


su0 = list_of_dfs[0].suburl.apply(avecrema)


su1 = list_of_dfs[1].suburl.apply(avecrema)


su2 = list_of_dfs[2].suburl.apply(avecrema)

#divido el df en lista de df de diez filas.
for i in range(len(list_of_dfs)):
    s = 'su'+str(i)
    s = list_of_dfs[i].suburl.apply(avecrema)
    time.sleep(randint(2, 5))


#url = 'https://www.axesor.es/buscar/empresas?q='+'Deoleo'+'#resultados'
#r = requests.post(url, data='Deoleo')


# Busqueda de cada empresa

#
#soup = BeautifulSoup(r.content,"html.parser")
#soup


#tabla = soup.findAll('table')
#tabla

#elemento = tabla[0].find_all('a')[0]
#elemento
#elemento.attrs

#suburl = 'https:'+elemento['href']


# Entro en la pagina con info de la empresa

#salvo_df= df
#salvo_df.to_csv('../data/segScra.csv')

#df.suburl[12]


#subtabla


#subelemento = subtabla[0].find_all('tr')[0]
#subelemento

#t = subelemento.text
#t


#tt = t.split(sep=':', maxsplit=-1)
#tt

# In[168]:



#tt = (t.split(sep=':', maxsplit=1))
#dictt = {tt[0]:tt[1]}
#dictt


#df = pd.DataFrame()
#df
#r = requests.get(suburl)
#print(r)
#print(r.headers)
#print(r.content)


#subsoup = BeautifulSoup(r.content,"html.parser")
#subsoup


#subtabla = subsoup.findAll('table')
#subtabla


#subelemento = subtabla[0].find_all('tr')[0]
#subelemento


#type(subelemento)


#subelemento.text


#subelemento.contents

#subelemento.text


# Para guardar en un df


#subelemento = subtabla[0].find_all('tr')[1]


#subelemento = 

#subelemento.text


#subelemento = subtabla[0].find_all('tr')[2]


#subelemento.text


#subelemento = subtabla[0].find_all('tr')[3]

#subelemento.text


##subelemento = subtabla[0].find_all('tr')[4]
#subelemento.text


#subelemento = subtabla[0].find_all('tr')[5]
#subelemento.text

#subelemento = subtabla[0].find_all('tr')[6]
#subelemento.text

#subelemento = subtabla[0].find_all('tr')[7]
#subelemento.text


#subelemento = subtabla[0].find_all('tr')[8]
#subelemento.text
#subelemento = subtabla[0].find_all('tr')[9]
#subelemento.text
#subelemento = subtabla[0].find_all('tr')[10]
#subelemento.text


#print(data.shape)
#data.info()
#data = data.drop('Email Address', axis = 1)

#data.info()
