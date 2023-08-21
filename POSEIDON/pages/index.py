import requests
import streamlit as sl

def pegarValores(n):

    url = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'

    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print('Erro na requisição')

sl.sidebar.title('Menu')
paginaSelecionada = sl.sidebar.selectbox('Selecione para onde você quer ir', ['Verificação','Dicas'])


if paginaSelecionada == 'Verificação':
    def interface():
        ## Teste Site ##
        max = pegarValores(0)['channel']['last_entry_id']

        sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">', unsafe_allow_html = True)
        sl.title('Consulte aqui o que você precisa')

        n = sl.text_input(' Digite quantidade dos últimos resultados que você quer:')

        try:
            n = int(n)

            if n > max or n < 1:
                raise Exception('Número fora de alcance')

            inteiro = True
            dados = pegarValores(n)

        except:
            f'Digite um número de 1 a {max}'

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

        cidade = sl.text_input('Digite a cidade que você quer receber as informações do clima:')
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

                    # aqui fica o card
                    sl.markdown(f'''
                    <div class="card"  style="width: 18rem;">
                        <img class="card-img-top" src="http://openweathermap.org/img/wn/01d@2x.png" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">{tempo["main"]} - {tempo["description"]}</h5>
                            <p class="card-text">_{dia}/{mes}/{ano}_</p>
                            <p>--{hora}--</p>
                            <a href="#" class="btn btn-primary">Go somewhere</a>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)   


                    sl.write(f'tempo: {tempo["main"]} - {tempo["description"]}')
                    sl.write(f'Vento: {vento["speed"]} - {vento["deg"]}º\n')

                    # sl.write(info)
            else:
                'Não foi possível encontrar o resultado pesquisado'
                sl.write(req)


    interface()
elif paginaSelecionada == 'Dicas' :
    sl.text ('salve')
