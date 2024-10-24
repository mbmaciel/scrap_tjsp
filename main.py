import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjsp/_search" # url do TJSP
api_key = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==" # Chave pública

payload = json.dumps({
  "size": 10000,
  "query": {
    "match": {"classe.codigo": 12729}  # 12729 (Exec. de Med. Alternativas)
  },
  "sort": [{"dataAjuizamento": {"order": "desc"}}] # ou asc
})

headers = {
  'Authorization': api_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)  # <Response [200]>
dados_dict = response.json() # <class 'dict'>
print(len(dados_dict))

#display(dados_dict['hits']['hits'][10])

processos = []

for processo in dados_dict['hits']['hits']:
  numero_processo = processo['_source']['numeroProcesso']
  grau = processo['_source']['grau']
  classe = processo['_source']['classe']['nome']
  assuntos = processo['_source']['assuntos'] # Pode ter mais de um
  data_ajuizamento = processo['_source']['dataAjuizamento']
  ultima_atualizacao = processo['_source']['dataHoraUltimaAtualizacao']
  formato = processo['_source']['formato']['nome']
  codigo = processo['_source']['orgaoJulgador']['codigo']
  orgao_julgador = processo['_source']['orgaoJulgador']['nome']
#  municipio = processo['_source']['orgaoJulgador']['codigoMunicipioIBGE']
  sort = processo['sort'][0]
  try:
    movimentos = processo['_source']['movimentos']
  except:
    movimentos = []

  processos.append([numero_processo, classe, data_ajuizamento, ultima_atualizacao, formato, \
                    codigo, orgao_julgador, grau, assuntos, movimentos, sort])

df = pd.DataFrame(processos, columns=['numero_processo', 'classe', 'data_ajuizamento', 'ultima_atualizacao', \
                      'formato', 'codigo', 'orgao_julgador', 'grau', 'assuntos', 'movimentos', 'sort'])

df.sample(5)

def converte_data(data_str):
    return pd.to_datetime(data_str)#.tz_convert('America/Sao_Paulo')


def gera_lista_assuntos(assuntos_do_df):
    lst_assuntos=[]
    for assunto in assuntos_do_df:
        try:
            lst_assuntos.append(assunto.get('nome'))
        except:
            lst_assuntos.append('')

    return lst_assuntos


def gera_lista_movimentos(movimentos):
    lst_movimentos_final =[]
    for movimento in movimentos:
        codigo = movimento.get('codigo')
        nome = movimento.get('nome')
        data_hora = movimento.get('dataHora')
        if data_hora:
            data_hora = converte_data(data_hora)
        lst_movimentos_final.append([codigo, nome, data_hora])
    return lst_movimentos_final

df['assuntos'] = df['assuntos'].apply(gera_lista_assuntos)
df['movimentos'] = df['movimentos'].apply(gera_lista_movimentos)
df['data_ajuizamento'] = df['data_ajuizamento'].apply(converte_data)
df['ultima_atualizacao'] = df['ultima_atualizacao'].apply(converte_data)
df['movimentos']= df['movimentos'].apply(lambda x: sorted(x, key=lambda tup: tup[2], reverse=False))
df.sample(5)
