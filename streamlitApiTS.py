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

    n = int(sl.text_input('nº de últimos resultados'))

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

# {"feeds": [{"created_at": "2023-05-17T18:46:16Z",
#             "entry_id": 54,
#             "field1": "8",
#             "field2": None,
#             "field3": None},
#            {"created_at": "2023-05-17T18:46:39Z",
#             "entry_id": 55,
#             "field1": "3",
#             "field2": None,
#             "field3": None},
#            {"created_at": "2023-05-17T18:47:00Z",
#             "entry_id": 56,
#             "field1": "0",
#             "field2": None,
#             "field3": None},
#            {"created_at": "2023-05-17T19:23:24Z",
#             "entry_id": 57,
#             "field1": "4",
#             "field2": None,
#             "field3": None},
#            {"created_at": "2023-06-28T23:53:01Z",
#             "entry_id": 58,
#             "field1": "0",
#             "field2": None,
#             "field3": None}]}
