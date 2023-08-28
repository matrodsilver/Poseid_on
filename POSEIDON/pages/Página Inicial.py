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
        if sl.button('Verificar') and inteiro == True and (0 < n <= dados['channel']['last_entry_id']):

            if dados is not None:
             
                bd = []

                tabGrafico, tabDados = sl.tabs(["Gráfico","Dados"])
                for numero in range(0, n):
                    try:
                        bd.append(float(dados['feeds'][numero]['field2']))
                    except:
                        bd.append(0)

                with tabGrafico:
                    sl.line_chart(bd)
                
                with tabDados:
                    sl.table(bd)

                # sl.write(dados)

        ## Teste Clima##
        token = '4127401294a510735af86031ebc9697b'

        cidade = sl.text_input('Digite a cidade que você quer receber as informações do clima:')
        codigoDoPais = 'BR'

        url5 = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'

        req = requests.get(url5)

        if sl.button('Consultar'):
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
                            <div class="card" style="width: 10rem;">
                                <img class="card-img-top" src="http://openweathermap.org/img/wn/{tempo["icon"]}@2x.png" alt="{tempo["main"]}">
                                <div class="card-body">
                                    <h3 class="card-title">{tempo["main"]} - {tempo["description"]}</h3>
                                    <h4 class="card-text">_{dia}/{mes}/{ano}_</h4>
                                    <h4>--{hora}--</h4>
                                    <h5>Vento: {vento["speed"]} - {vento["deg"]}º</h5>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                    # sl.write(info)
            else:
                'Não foi possível encontrar o resultado pesquisado'
                sl.write(req)

    interface()
elif paginaSelecionada == 'Dicas' :
    sl.markdown('''
<h3>Preserve o Nosso Meio Ambiente: Não Jogue Lixo na Rua ou nos Bueiros</h3>

Em nosso dia a dia agitado, muitas vezes, esquecemos o impacto que nossas ações podem ter no meio ambiente. Uma dessas ações é o descarte inadequado de lixo, especialmente nas ruas e bueiros. Parece inofensivo, mas o que você joga na rua ou nos bueiros tem consequências sérias para o nosso planeta e para a qualidade de vida de todos nós.

1. Poluição Ambiental: Quando jogamos lixo na rua, ele não desaparece magicamente. Em vez disso, é carregado pela chuva para os bueiros e, eventualmente, para os rios e oceanos. Isso polui nossos preciosos recursos hídricos e ameaça a vida marinha.

2. Inundações: Os bueiros entupidos com lixo podem obstruir o fluxo de água da chuva. Isso aumenta o risco de inundações, causando danos materiais e colocando vidas em perigo.

3. Saúde Pública: Lixo nas ruas atrai pragas, cria condições insalubres e aumenta o risco de doenças. Ninguém quer viver em um ambiente sujo e doente.

4. Beleza Natural e Estética: Jogue lixo na rua e você estará contribuindo para a degradação da beleza natural de sua cidade. Lixeiras e contentores de reciclagem estão amplamente disponíveis para manter nossas ruas limpas e agradáveis.

5. Responsabilidade Coletiva: Preservar o meio ambiente não é apenas responsabilidade do governo ou de organizações ambientais. Cada um de nós tem um papel a desempenhar. Pequenas ações individuais podem criar um grande impacto positivo quando se trata de manter nosso planeta saudável.

<h4>E então o que você pode fazer?</h4>
<ul>
    <li>
        Descarte Responsável: Sempre leve seu lixo até uma lixeira adequada ou contentor de reciclagem. Ensine as crianças desde cedo a fazer o mesmo.
    </li>
    <li>
        Recicle: Separe seu lixo reciclável do lixo comum. A reciclagem ajuda a reduzir a quantidade de lixo que vai parar nos aterros sanitários.
    </li>
    <li>
        Participe de Campanhas de Limpeza: Una-se a grupos locais que realizam limpezas regulares em sua comunidade. É uma maneira eficaz de fazer a diferença.
    </li>
    <li>
        Eduque os Outros: Compartilhe informações sobre a importância de não jogar lixo na rua e nos bueiros com amigos e familiares. Quanto mais pessoas estiverem cientes, maior será o impacto positivo.
    </li>
</ul>

<h6>Cada ação conta. Vamos trabalhar juntos para manter nossas ruas limpas, nossos bueiros desobstruídos e nosso planeta saudável para as futuras gerações. A mudança começa com você!</h6>
''', unsafe_allow_html= True)
