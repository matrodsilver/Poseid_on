import requests
import streamlit as sl


def selecionarUsuarios(n):

    url = f"https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}"

    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print("Erro na requisição")


def interface():
    # sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">')
    sl.title('consulta dados TS')

    'teste escrita só em string'  # site escreve strings

    n = sl.text_input('nº de últimos resultados')

    try:
        n = int(n)
    except:
        'digite um número'

    if sl.button('consultar'):

        dados = selecionarUsuarios(n)

        if dados is not None:

            bd = []

            for numero in range(0, n):
                bd.append(int(dados['feeds'][numero]['field1']))

            sl.line_chart(bd)
            sl.write(bd)

            sl.write(dados)


interface()
