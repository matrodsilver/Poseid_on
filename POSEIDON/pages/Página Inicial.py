'''Este código fornece ao usuário vizualização da base de dados sensorial e do clima'''

import requests # biblioteca para comunicação com links
import streamlit as sl # biblioteca para a confecção de sites
import pandas as p # biblioteca para a organização de dados


sl.sidebar.title('Menu') # menu para seleção de páginas
paginaSelecionada = sl.sidebar.selectbox('Selecione a página a ser exibida', ['Verificação', 'Dicas'])


if paginaSelecionada == 'Verificação':

  # função responsável por requisitar os dados na nuvem (se possível)
  def pegarValores(n):

    urlDados = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'
    urlClima = f'https://api.thingspeak.com/channels/2244673/feeds.json?api_key=FOKGIHJ79MUZHIFW&results={n}'

    respostaDados = requests.get(urlDados)
    respostaClima = requests.get(urlClima)

    if respostaDados.status_code == 200: # se foi possível retornar os dados

      return [respostaDados.json(), respostaClima.json()] # retorna os arquivos json com os dados requisitados
    
    else:
      'Erro na requisição'
      return {} # retorna uma string vazia e que a requisição teve um erro
    

  # função responsável por processar os inputs do usuário, organiza-los e retorna-los de maneira a serem facilmente visualizados
  def interface():
    dados = None
    max = pegarValores(0)[0]['channel']['last_entry_id'] # variável com o valor máximo

    sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">', unsafe_allow_html=True)
    sl.title('Consulte aqui as informações necessárias')


    ## Dados do Sensoriamento ##
    n = sl.text_input(
        f'Quantidade dos últimos resultados a serem exibidos:')

    try: # testar se valor inserido é válido
      n = int(n)

      if n > max or n < 1:
        raise Exception('Número fora de alcance')

      dados = pegarValores(n)[0]
      clima = pegarValores(n)[1]

    except: # se não é, informar que valor digitado não é válido, e exibir os 15 últimos dados
      n = 15
      
      dados = pegarValores(n)[0]
      clima = pegarValores(n)[1]

      sl.markdown(f'''<h6 style ="height: 0rem; color: #808080; ">Digite um número de 1 a {max}</h6>
                  <h6 style ="height: 0rem; color: #808080; ">Exibindo os 15 resultados mais recentes</h6>''', unsafe_allow_html=True)


    if dados is not None:

      # inicialização de variáveis para armazenamento de dados até sua exibição
      bd = []
      bdClima = {'Descrição':{}, 'Categoria':{}, 'Umidade':{}, 'Probabilidade de Chuva':{}, 'Vento Velocidade':{}, 'Vento Angulo':{}}
      horario = []
      horarioMin = []
      horarioClima = []

      tabGrafico, tabDados, tabClimaRegistrado = sl.tabs(["Gráfico", "Dados", "Clima Registrado"])

      # para a quantidade de valores requisitada, o valor é colocado em sua respectiva posição na base de dados e armazenado para ser exibido
      for numero in range(n):

        # Referente aos dados dos sensores

        dataBR = dados['feeds'][numero]['created_at']

        dia = dataBR[8:10]
        mes = dataBR[5:7]
        ano = dataBR[:4]
        hora = dataBR[11:19]

        horario.append(f'{dia}/{mes}/{ano} {hora}')
        horarioMin.append(f'{dia}/{mes} {hora}')

        try:
          if float(dados['feeds'][numero]['field2']) > 0:
            bd.append(float(dados['feeds'][numero]['field2']))
          else:
            bd.append(0)

        except:
          bd.append(0)
        
        
        # Dados do clima

        dataClima = clima['feeds'][numero]['created_at']

        diaClima = dataClima[8:10]
        mesClima = dataClima[5:7]
        anoClima = dataClima[:4]
        horaClima = dataClima[11:19]

        horarioClima.append(f'{diaClima}/{mesClima}/{anoClima} {horaClima}')
          
        bdClima['Descrição'][horarioClima[numero]] = clima['feeds'][numero]['field1']
        bdClima['Categoria'][horarioClima[numero]] = clima['feeds'][numero]['field2']
        bdClima['Umidade'][horarioClima[numero]] = str(clima['feeds'][numero]['field4'])+'%'
        bdClima['Probabilidade de Chuva'][horarioClima[numero]] = str(clima['feeds'][numero]['field3']) # * 100)+'%'
        bdClima['Vento Velocidade'][horarioClima[numero]] = str(clima['feeds'][numero]['field5'])+'km/h'
        bdClima['Vento Angulo'][horarioClima[numero]] = str(clima['feeds'][numero]['field6'])+'°'


      dicionarioDados = {}
      dicionarioDadosMin = {}


      # debug: Ex. de como é necessário formatar os dados

      # dicionarioClima = {'Categoria': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
      #                    'Descrição': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
      #                     'Umidade': {'data1':f'{1}%','data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
      #                     'Probabilidade de Chuva': {'data1':f'{1}%', 'data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
      #                     'Vento Velocidade': {'data1':f'{1}km/h', 'data2': f'{2}km/h', 'data3': f'{3}km/h', 'data4': f'{4}km/h'},
      #                     'Vento Angulo': {'data1':f'{1}º', 'data2': f'{2}º', 'data3': f'{3}º', 'data4': f'{4}º'}}


      for n in range(0, len(bd)): # para cada valor, salva a data com seu respectivo valor
        dicionarioDados[str(horario[n])] = bd[n]
        dicionarioDadosMin[str(horarioMin[n])] = bd[n]

      grafico = p.DataFrame({'Data': dicionarioDadosMin.keys(), 'Medição (cm)': dicionarioDadosMin.values()}) # armazena o dicionário como um frame de dados, para nomeação dos eixos

      with tabGrafico: # exibir gráfico
        sl.area_chart(grafico, x='Data', y='Medição (cm)')

      with tabDados: # exibir tabela
        # debug: dicionarioDados = [str(v)+' cm' for v in dicionarioDados.values()] # tentativa de colocar cm na frente de cada valor (mas data sai do index)
        
        sl.table(dicionarioDados)
      
      with tabClimaRegistrado: # exibir dados do clima no momento do envio dos dados
        sl.line_chart(bdClima)
        sl.table(bdClima)


    ## Referente ao clima ##

    token = '4127401294a510735af86031ebc9697b' # chave da conta usada para requisição

    cidade = sl.text_input('Digite a cidade a qual deseja consultar informações climáticas:')
    codigoDoPais = 'BR'

    url5dias = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'

    req5 = requests.get(url5dias)

    if sl.button('Consultar'):
      if req5.status_code == 200: # se dados foram recolhidos

        info = req5.json()

        ultimoDia = 0

        for n in range(len(info['list'])): # para cada valor, 

          # referenciamento de valores em suas respectivas variáveis
          dadosClima = info['list'][n]['weather'][0]

          data = info['list'][n]['dt_txt']
          descricaoGeral = dadosClima['main']
          descricaoFiltrada = dadosClima['description']
          ventoVelocidade = info['list'][n]['wind']['speed']
          ventoAngulo = info['list'][n]['wind']['deg']
          umidade = info['list'][n]['main']['humidity']
          probabilidadeDeChuva = info['list'][n]['pop']

          icone = dadosClima["icon"]

          # debug: considerar variáveis
          # visibilidade =
          # nuvens =

          dia = data[8:10]
          mes = data[5:7]
          ano = data[0:4]
          hora = data[11:16]

          # função que retorna uma cor de acordo com o valor do parâmetro
          def cor(prob):
            prob = round(prob * 100)
            prob2 = round(99 - prob)

            if prob > 99:
              prob = 99
            if prob2 < 0:
              prob2 = 0

            # para valor de vermelho
            if len(str(prob)) < 2:
              add = ''

              while len(str(add)) < 2 - len(str(prob)):
                add += '0'

              add += f'{prob}'

              prob = add

            # para valor de verde
            if len(str(prob2)) < 2:
              add = ''

              while len(str(add)) < 2 - len(str(prob2)):
                add += '0'

              add += f'{prob2}'

              prob2 = add

            hex = f'#{prob}{prob2}00'

            return hex # retorna uma cor no formato hex # debug: de 0 a 99

          # função que retorna uma string se valor do parâmetro indica a presença de água
          def recomendar(var):
            if type(var) == float: # se valor é é float

              if var > .98: # se o float é maior que 98%
                return '(Chuva é certa, coleta não recomendada)'
              else:
                return ''
            
            else: # (basicamente) se é string

              if var == 'Rain': # se têm chuva
                return '(Clima chuvoso, coleta não recomendada)'
              else:
                return ''

          card = '' # inicializa variável de texto que será o card

          if dia != ultimoDia: # se o dia é diferente do último dia, "card" é resetado

            ultimoDia = dia

            card += f'''<h1 class="card-text" style="height: 4rem;">{dia}/{mes}/{ano}</h1>
            <h6 class="card-text" style="height: 0rem;"> ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾</h6>'''

          card += f'''<h3 style="height: .0rem;">{hora}</h3>
          <h6 class="card-text" style="height: 0rem;">‾‾‾‾‾‾‾‾</h6>
          <img class="card-img-top" src="http://openweathermap.org/img/wn/{icone}@2x.png" alt="{descricaoGeral}" style="width: 10rem; height: 10rem;">
          <h5 style="height: 0rem;">{descricaoGeral}: {descricaoFiltrada} <span style="height: 0rem; color: #990000">{recomendar(descricaoGeral)}</span></h5>
          <h5 style="height: 0rem;">Umidade: {umidade}%</h5>
          <h5 style="height: 0rem;">Probabilidade de Precipitação: <span style="height: 0rem; color: {cor(probabilidadeDeChuva)}">{round(probabilidadeDeChuva * 100)}% {recomendar(probabilidadeDeChuva)}</span></h5>
          <h5 style="height: 0rem;">Vento: {ventoVelocidade} a {ventoAngulo}º</h5>
          <h6 style="height: 0rem;"></h6>'''
          
          sl.markdown(card, unsafe_allow_html=True)

      else:
        'Não foi possível encontrar o resultado pesquisado'

  interface()

elif paginaSelecionada == 'Dicas':
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
''', unsafe_allow_html=True)
