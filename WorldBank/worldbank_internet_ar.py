
import json
import requests
import urllib
import pandas as pd
from google.colab import files

#lista com as abreviações/codigos de paises que serão puxados
cod_paises=["BR","AR","CL","PE","BO","UY","CO","VE","EC","PR","PY"]

df_merged=pd.DataFrame()

# função para puxar os dados
def getResults(url):
  try:
   response = requests.get(url)
   dados = response.json()
   return dados
  except Exception as eror:
   print("Erro: ", eror)
   return None


# loop que puxa os dados para cada codigode país e inclui num dataframe final a coluna com os valores puxados
for cod_pais in cod_paises:
   pais=cod_pais

   api_url="https://api.worldbank.org/v2/country/" + pais +"/indicator/IT.NET.USER.ZS?format=json"
   dados_gerados = getResults(api_url)
   df = pd.DataFrame(dados_gerados[1])
   print(cod_pais)
   df_final = df[['date', 'value']]
   df_final = df_final.rename(columns={"value": "value_"+cod_pais})


   if df_merged.empty:
        df_merged = df_final
   else:
      df_merged = pd.merge(df_merged, df_final, on='date', how='left')


nome_arquivo="porcento_acesso_internet"
csv_name = nome_arquivo +".csv"
arquivo = df_merged.to_csv(csv_name,index=False)
files.download(csv_name)