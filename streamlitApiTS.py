'''Código igual mas esse texto adicionado pra testar branches do GIT'''

import requests
import streamlit as sl


def pegarValores(n):

    url = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'

    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print('Erro na requisição')


def interface():
    ## Teste Site ##
    max = pegarValores(0)['channel']['last_entry_id']

    # sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">')
    sl.title('consulta dados TS')

    'teste escrita só em string'  # site escreve strings

    n = sl.text_input('nº de últimos resultados')

    try:
        n = int(n)

        if n > max or n < 1:
            raise Exception('número fora de alcance')

        inteiro = True
        dados = pegarValores(n)

    except:
        f'digite um número de 1 a {max}'

        inteiro = False

    # teste condicional de funcionamento
    if sl.button('consultar') and inteiro == True and (0 < n <= dados['channel']['last_entry_id']):

        if dados is not None:

            bd = []

            for numero in range(0, n):
                bd.append(int(dados['feeds'][numero]['field1']))

            sl.line_chart(bd)
            sl.table(bd)

            # sl.write(dados)

    ## Teste Clima##
    token = '4127401294a510735af86031ebc9697b'

    cidade = sl.text_input('digite uma cidade')
    codigoDoPais = 'BR'

    url5 = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'

    req = requests.get(url5)

    if sl.button('clima'):
        if req.status_code == 200:

            info = req.json()

            ultimoDia = 0

            for n in range(0, len(info['list'])):
                tempo = info['list'][n]['weather'][0]
                vento = info['list'][n]['wind']
                data = info["list"][n]["dt_txt"]

                dia = data[8:10]
                mes = data[5:7]
                ano = data[0:4]
                hora = data[11:16]

                if dia != ultimoDia:
                    # dois espaços no final da linha fazem o mesmo que '\n' no streamlit
                    sl.write(f'''__ __{dia}/{mes}/{ano}__ __  
                             --{hora}--''')

                    ultimoDia = dia
                else:
                    sl.write(f'--{hora}--')

                sl.write(f'tempo: {tempo["main"]} - {tempo["description"]}')
                sl.write(f'Vento: {vento["speed"]} - {vento["deg"]}º\n')

                # sl.write(info)
        else:
            'erro'
            sl.write(req)


interface()

'''
informações relevantes:
weather
wind
dt_txt
pop
rain
city
'''
