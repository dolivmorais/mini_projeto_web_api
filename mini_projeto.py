import requests
from pprint import pprint
import pandas as pd

import streamlit as st

def fazer_requests(url, params=None):
    resposta = requests.get(url, params=params)

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        print("Resposta:")
        resultado = resposta.json()
    return resultado


def pegar_nome_por_decada(nome):
    url = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    dados_decadas = fazer_requests(url=url)
    if not dados_decadas:
        return {}
    dict_decadas = {}
    for dados in dados_decadas[0]['res']:
        decada = dados['periodo']
        quantidade = dados['frequencia']
        dict_decadas[decada] = quantidade
    return dict_decadas



def main():
    st.title('Web App Nomes')
    st.write('Dados do IBGE (fonte: https://servicodados.ibge.gov.br/api/docs/localidades#api-Municipios-municipiosGet)')

    nome = st.text_input ('Consulte um nome: ')
    if not nome:
        st.stop()

    dict_decadas = pegar_nome_por_decada(nome)
    if not dict_decadas:
        st.warning(f'Não existe dados para o nome {nome} pesquisado')
        st.stop()
    
    df = pd.DataFrame.from_dict(dict_decadas, orient='index')

    col1, col2 = st.columns([0.3,0.7])
    with col1:
        st.write('Frenquecia por decada')
        st.dataframe(df)
    with col2:
        st.write("Evolução por decada")
        st.line_chart(df)

if __name__ == '__main__':
    main()