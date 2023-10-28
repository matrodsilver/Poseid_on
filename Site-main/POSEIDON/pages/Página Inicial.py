import requests
import streamlit as sl
import pandas as p




def pegarValores(n):

  urlDados = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'
  urlClima = f'https://api.thingspeak.com/channels/2244673/feeds.json?api_key=FOKGIHJ79MUZHIFW&results={n}'

  urlSim = 'https://api.thingspeak.com/channels/2316505/feeds.json?results=2' # "results" em branco resulta em todos os dados

  respostaDados = requests.get(urlDados)
  respostaClima = requests.get(urlClima)

  respostaSim = requests.get(urlSim)

  if respostaDados.status_code == 200 and respostaClima.status_code == 200 and respostaSim.status_code == 200:

    return [respostaDados.json(), respostaClima.json(), respostaSim.json()] # [medidas, clima, dados simulando outros sistemas Poseid.on]
  else:
    print('Erro na requisição')
    return [respostaDados.json(), respostaClima.json(), respostaSim.json()]


sl.sidebar.title('Menu')
paginaSelecionada = sl.sidebar.selectbox(
    'Selecione a página a ser exibida', ['Verificação', 'Dicas'])


if paginaSelecionada == 'Verificação':
  def interface():
    volumes = None

    max = pegarValores(0)[1]['channel']['last_entry_id']

    sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">', unsafe_allow_html=True)
    sl.title('Consulte aqui as informações necessárias')

    n = sl.text_input(
      f'Quantidade dos últimos resultados a serem exibidos:')

    try:
      n = int(n)

      if n > max or n < 1:
        raise Exception('Número fora de alcance')

      volumes = pegarValores(n)[0] # dados do volume do sistema
      clima = pegarValores(n)[1] # dados do clima no local do sistema durante o envio de dados

    except:
      n = 15

      volumes = pegarValores(n)[0]
      clima = pegarValores(n)[1]

      sl.markdown(f'''<h6 style ="height: 0rem; color: #808080; ">Digite um número de 1 a {max}</h6>
                  <h6 style ="height: 0rem; color: #808080; ">Exibindo os 15 resultados mais recentes</h6>''', unsafe_allow_html=True)
    if sl.button:
      
    # teste condicional de funcionamento
      if volumes is not None:

        bdVolumes = [] # banco de dados com valores dos volumese respectivas datas
        bdClima = {'Descrição': {}, 'Categoria': {}, 'Umidade': {},
                  'Chuva á 1H': {}, 'Vento Velocidade': {}, 'Vento Angulo': {}}
        
        bdClimaGrafico = {'Descrição': {}, 'Umidade': {},
                          'Chuva á 1H': {}} # banco de dados para exibição no gráfico

        horario = []
        horarioGrafico = []
        horarioClima = []
        horarioClimaGráfico = []

        tabGrafico, tabTabela, tabClimaRegistrado, tabBueiros = sl.tabs(
            ["Gráfico", "Tabela", "Clima", "Estado atual dos sistemas"])
        for numero in range(n):

          # __Dados dos sensores__
          dataBR = volumes['feeds'][numero]['created_at']

          dia = dataBR[8:10]
          mes = dataBR[5:7]
          ano = dataBR[:4]
          hora = str(int(dataBR[11:13])-1) + dataBR[13:19] # arrumando fuso-horário

          horario.append(f'{dia}/{mes}/{ano} {hora}')
          horarioGrafico.append(f'{dia}/{mes} {hora}')

          try:
            valorDoVolume = float(volumes['feeds'][numero]['field2'])
          except:
            valorDoVolume = 0

          try:
            if 0 <= (57 - valorDoVolume) <= 38:
              bdVolumes.append(57 - valorDoVolume)
            else:
              bdVolumes.append(38)

          except:
            bdVolumes.append(38)

          dataClima = clima['feeds'][numero]['created_at']

          diaClima = dataClima[8:10]
          mesClima = dataClima[5:7]
          anoClima = dataClima[:4]
          horaClima = dataClima[11:19]

          horarioClima.append(f'{diaClima}/{mesClima}/{anoClima} {horaClima}')
          horarioClimaGráfico.append(f'{diaClima}/{mesClima} {horaClima}')

          bdClima['Descrição'][horarioClima[numero]
                              ] = clima['feeds'][numero]['field1']
          bdClima['Categoria'][horarioClima[numero]
                              ] = clima['feeds'][numero]['field2']
          bdClima['Umidade'][horarioClima[numero]] = str(
              clima['feeds'][numero]['field4'])+' %'
          bdClima['Chuva á 1H'][horarioClima[numero]] = str(
              clima['feeds'][numero]['field3'])+' mm'
          bdClima['Vento Velocidade'][horarioClima[numero]] = str(
              clima['feeds'][numero]['field5'])+' km/h'
          bdClima['Vento Angulo'][horarioClima[numero]] = str(
              clima['feeds'][numero]['field6'])+'°'

          if clima['feeds'][numero]['field1'] == "'rain'":
            bdClimaGrafico['Descrição'][horarioClimaGráfico[numero]
                                        ] = 'Chuva Registrada'
          else:
            bdClimaGrafico['Descrição'][horarioClimaGráfico[numero]
                                        ] = 'Chuva não fichada'

          bdClimaGrafico['Umidade'][horarioClimaGráfico[numero]] = str(
              clima['feeds'][numero]['field4'])+' %'
          bdClimaGrafico['Chuva á 1H'][horarioClimaGráfico[numero]] = str(
              clima['feeds'][numero]['field3'])+' mm'

        dadosGerais = {}
        dadosGrafico = {}

        for n in range(0, len(bdVolumes)):
          dadosGerais[str(horario[n])] = bdVolumes[n]
          dadosGrafico[str(horarioGrafico[n])] = bdVolumes[n]

        grafico = p.DataFrame({'Data': dadosGrafico.keys(
        ), 'Medição (cm)': dadosGrafico.values()})

        with tabGrafico:
          sl.area_chart(grafico, x='Data', y='Medição (cm)')

          Media = int(round(sum(dadosGerais.values()) / len(dadosGerais)))

          r, g, b = int(round(Media*6.7105263157894736842105263157895)
                        ), int(round(255 - Media*6.7105263157894736842105263157895)), 0

          hex = "#%02x%02x%02X" % (r, g, b)

          sl.markdown(
              f'''<h6 style="height: 2rem; color: #808080; ">Média: <span style="height: 0rem; color: {hex}">{Media} cm de volume ocupado</span></h6>''', unsafe_allow_html=True)  # (arredondamento da soma dos valores / quantidade de valores) - 19(distância onde começa a contagem (mínima))

        with tabTabela:

          sl.table(dadosGerais)

        with tabClimaRegistrado:
          sl.line_chart(bdClimaGrafico)
          sl.table(bdClima)

        with tabBueiros:
          volumesSim = pegarValores(1)[2]  # 1 é um valor arbitrário, pois a função sempre retornará o valor máximo
          
          atual1 = float(volumesSim['feeds'][len(volumesSim)-1]['field1'])
          atual2 = float(volumesSim['feeds'][len(volumesSim)-1]['field2'])
          atual3 = float(volumesSim['feeds'][len(volumesSim)-1]['field3'])
          
          atual = {str(atual1): "CAMPINAS", str(atual2): "SÃO PAULO", str(atual3): "ALPHAVILLE", str(round(bdVolumes[-1], 2)): "ACLIMAÇÃO"}
          # ordemAtual = sorted(atual)

          decrescente = []

          for chave in atual.keys():
            decrescente.append(float(chave))

          decrescente = sorted(decrescente)

          r1, g1, b1 = round(decrescente[0] * 6.7105263157894736842105263157895), round(255 - float(decrescente[0]) * 6.7105263157894736842105263157895), 0
          hex1 = "#%02x%02x%02X" % (r1, g1, b1)

          r2, g2, b2 = round(decrescente[1] * 6.7105263157894736842105263157895), round(255 - decrescente[1] * 6.7105263157894736842105263157895), 0
          hex2 = "#%02x%02x%02X" % (r2, g2, b2)

          r3, g3, b3 = round(decrescente[2] * 6.7105263157894736842105263157895), round(255 - decrescente[2] * 6.7105263157894736842105263157895), 0
          hex3 = "#%02x%02x%02X" % (r3, g3, b3)

          r4, g4, b4 = round(decrescente[3] * 6.7105263157894736842105263157895), round(
            255 - decrescente[3] * 6.7105263157894736842105263157895), 0
          hex4 = "#%02x%02x%02X" % (r4, g4, b4)


          sl.markdown(
            f'''<h4 style="height: 3rem; color: #606060;">Prioridade atual dos sistemas Poseid.on:</h4>
            <h6 style="height: 2rem; color: #000000;">{atual[str(decrescente[0])]} em <span style="height: 0rem; color: {hex4}">{decrescente[3]}cm</span> de volume ocupado</h6>
            <h6 style="height: 2rem; color: #000000;">{atual[str(decrescente[1])]} em <span style="height: 0rem; color: {hex3}">{decrescente[2]}cm</span> de volume ocupado</h6>
            <h6 style="height: 2rem; color: #000000;">{atual[str(decrescente[2])]} em <span style="height: 0rem; color: {hex2}">{decrescente[1]}cm</span> de volume ocupado</h6>
            <h6 style="height: 2rem; color: #000000;">{atual[str(decrescente[3])]} em <span style="height: 0rem; color: {hex1}">{decrescente[0]}cm</span> de volume ocupado</h6>''', unsafe_allow_html=True)  # (arredondamento da soma dos valores / quantidade de valores) - 19(distância onde começa a contagem (mínima))

    ## Clima ##
    token = '4127401294a510735af86031ebc9697b'

    cidade = sl.text_input(
        'Digite a cidade a qual deseja consultar informações climáticas:')
    codigoDoPais = 'BR'

    url5dias = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'

    req5 = requests.get(url5dias)

    if sl.button('Consultar'):
      if req5.status_code == 200:

        info = req5.json()

        ultimoDia = 0

        for n in range(len(info['list'])):
          dadosClima = info['list'][n]['weather'][0]

          data = info['list'][n]['dt_txt']
          descricaoGeneralizada = dadosClima['main']
          descricaoFiltrada = dadosClima['description']
          ventoVelocidade = info['list'][n]['wind']['speed']
          ventoAngulo = info['list'][n]['wind']['deg']
          umidade = info['list'][n]['main']['humidity']
          probabilidadeDeChuva = info['list'][n]['pop']

          icone = dadosClima["icon"]

          dia = data[8:10]
          mes = data[5:7]
          ano = data[0:4]
          hora = data[11:16]

          r, g, b = int(round(probabilidadeDeChuva * 255)), 255 - \
              int(round(probabilidadeDeChuva * 255)), 0

          hex = "#%02x%02x%02X" % (r, g, b)

          def recomendar(var):
            if var == 1:  # se var é 100%
              return '<h6 style="height: 0rem; color: #FF0000">Chuva é certa, coleta não recomendada</h6>'

            else:  # se é string
              if var == 'Rain':
                return '<h6 style="height: 0rem; color: #FF0000">Clima chuvoso, coleta não recomendada</h6>'
              else:
                return ''

          card = ''

          if dia != ultimoDia:
            ultimoDia = dia

            card += f'''<h1 class="card-text" style="height: 4rem;">{dia}/{mes}/{ano}</h1>
            <h6 class="card-text" style="height: 0rem;"> ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾</h6>'''

          card += f'''<h3 style="height: .0rem;">{hora}</h3>
          <h6 class="card-text" style="height: 0rem;">‾‾‾‾‾‾‾‾</h6>
          <img class="card-img-top" src="http://openweathermap.org/img/wn/{icone}@2x.png" alt="{descricaoGeneralizada}" style="width: 10rem; height: 10rem;">
          <h5 style="height: 0rem;">{descricaoGeneralizada}: {descricaoFiltrada}</h5>{recomendar(descricaoGeneralizada)}
          <h5 style="height: 0rem;">Umidade: {umidade}%</h5>
          <h5 style="height: 0rem;">Probabilidade de Precipitação: <span style="height: 0rem; color: {hex}">{round(probabilidadeDeChuva * 100)}%</span>{recomendar(probabilidadeDeChuva)}</h5>
          <h5 style="height: 0rem;">Vento: {ventoVelocidade} km/h a {ventoAngulo}º</h5>
          <h6 style="height: 0rem;"></h6>'''

          # aqui fica o card
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
