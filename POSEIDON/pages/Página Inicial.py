import requests
import streamlit as sl
import pandas as p


def pegarValores(n):

  url = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'

  resposta = requests.get(url)
  if resposta.status_code == 200:
    return resposta.json()
  else:
    print('Erro na requisição')
    return {}


sl.sidebar.title('Menu')
paginaSelecionada = sl.sidebar.selectbox(
    'Selecione a página a ser exibida', ['Verificação', 'Dicas'])


if paginaSelecionada == 'Verificação':
  def inicial():
    dados = pegarValores(15)
    bd = []
    horario = []
    horarioMin = []

    tabGrafico, tabDados = sl.tabs(["Gráfico", "Dados"])
    for numero in range(0, 15): # type: ignore
          
        dataBR = dados['feeds'][numero]['created_at']
        
        dia = dataBR[8:10]
        mes = dataBR[5:7]
        ano = dataBR[:4]
        hora = dataBR[11:19]
        
        horario.append(f'{dia}/{mes}/{ano} {hora}')
        horarioMin.append(f'{dia}/{mes} {hora}')

        # opção 1
        try:
          if float(dados['feeds'][numero]['field2']) > 0:
            bd.append(float(dados['feeds'][numero]['field2']))
          else:
            bd.append(0)
            
        except:
          bd.append(0)
          
        # # opção 2
        # try:
        #   if float(dados['feeds'][numero]['field2']) > 0:
        #     bd.append(float(dados['feeds'][numero]['field2']))
          
        #   else: #(implícito na lógica)
        #   # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
        #     pass
        
        # except:
        # # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
        #   pass

    dicionarioDados = {}
    dicionarioDadosMin = {}
    for n in range(0, len(bd)):
      dicionarioDados[str(horario[n])] = bd[n]
      dicionarioDadosMin[str(horarioMin[n])] = bd[n]

    with tabGrafico:
      sl.area_chart(dicionarioDadosMin)

    with tabDados:
      sl.table(dicionarioDados)
    
    
  def interface():
    ## Teste Site ##
    dados = None
    max = pegarValores(0)['channel']['last_entry_id']

    sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">', unsafe_allow_html=True)
    sl.title('Consulte aqui as informações necessárias')

    n = sl.text_input(
        f'Quantidade dos últimos resultados a serem exibidos:')

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
    if sl.button('Verificar') and inteiro == True and (0 < n <= dados['channel']['last_entry_id']): # type: ignore

      if dados is not None:

        bd = []
        horario = []
        horarioMin = []

        tabGrafico, tabDados = sl.tabs(["Gráfico", "Dados"])
        for numero in range(0, n): # type: ignore
          
          dataBR = dados['feeds'][numero]['created_at']
          
          dia = dataBR[8:10]
          mes = dataBR[5:7]
          ano = dataBR[:4]
          hora = dataBR[11:19]
          
          horario.append(f'{dia}/{mes}/{ano} {hora}')
          horarioMin.append(f'{dia}/{mes} {hora}')

          # opção 1
          try:
            if float(dados['feeds'][numero]['field2']) > 0:
              bd.append(float(dados['feeds'][numero]['field2']))
            else:
              bd.append(0)
              
          except:
            bd.append(0)
            
          # # opção 2
          # try:
          #   if float(dados['feeds'][numero]['field2']) > 0:
          #     bd.append(float(dados['feeds'][numero]['field2']))
            
          #   else: #(implícito na lógica)
          #   # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
          #     pass
          
          # except:
          # # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
          #   pass
        
        dicionarioDados = {}
        dicionarioDadosMin = {}
        for n in range(0, len(bd)):
          dicionarioDados[str(horario[n])] = bd[n]
          dicionarioDadosMin[str(horarioMin[n])] = bd[n]

        with tabGrafico:
          sl.area_chart(dicionarioDadosMin)

        with tabDados:
          sl.table(dicionarioDados)

        # sl.write(dados)

    ## Clima ##
    token = '4127401294a510735af86031ebc9697b'

    cidade = sl.text_input(
        'Digite a cidade a qual deseja consultar informações climáticas:')
    codigoDoPais = 'BR'

    # FIAP(lat, long) = -23.57323583564156, -46.623008521519246

    url5dias = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'
    # urlCurrent = f'https://api.openweathermap.org/data/2.5/weather?lat={-23.57323583564156}&lon={-46.623008521519246}&appid={token}&units=metric&lang={"pt_br"}'
    # urlMapa = f'https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}&units=metric&lang={"pt_br"}'
    # urlGeo = f'http://api.openweathermap.org/geo/1.0/direct?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'
    # urlTrigger = f'http://api.openweathermap.org/data/3.0/triggers'
    
    req5 = requests.get(url5dias)
    # reqCurrent = requests.get(urlCurrent)
    # reqMapa = requests.get(urlMapa)
    # reqGeo = requests.get(urlGeo)
    # reqTrigger = requests.get(urlTrigger)

    if sl.button('Consultar'):
      if req5.status_code == 200:

        info = req5.json()

        ultimoDia = 0
        ultimaHora = 0
        
        for n in range(len(info['list'])):
          dadosClima = info['list'][n]['weather'][0]

          data = info['list'][n]['dt_txt']
          descricaoGeral = dadosClima['main']
          descricaoFiltrada = dadosClima['description']
          ventoVelocidade = info['list'][n]['wind']['speed']
          ventoAngulo = info['list'][n]['wind']['deg']
          umidade = info['list'][n]['main']['humidity']
          probabilidadeDeChuva = info['list'][n]['pop']
          
          icone = dadosClima["icon"]
          
          #visibilidade = 
          #nuvens =
          
          
          teste = {'Descrição': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
                   'Filtrada': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
                   
                   'Visualização': {'data1':1, 'data2': 2, 'data3': 3, 'data4': 4}, # debug
                   
                   'Umidade': {'data1':f'{1}%','data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
                   'Probabilidade de Chuva': {'data1':f'{1}%', 'data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
                   'Vento Velocidade': {'data1':f'{1}km/h', 'data2': f'{2}km/h', 'data3': f'{3}km/h', 'data4': f'{4}km/h'},
                   'Vento Angulo': {'data1':f'{1}º', 'data2': f'{2}º', 'data3': f'{3}º', 'data4': f'{4}º'}} # debug


          dia = data[8:10]
          mes = data[5:7]
          ano = data[0:4]
          hora = data[11:16]

          
          card = ''


          if dia != ultimoDia:
            ultimoDia = dia
            
            card += f'''<h1 class="card-text" style="height: 4rem;">{dia}/{mes}/{ano}</h1>
            <h6 class="card-text" style="height: 0rem;"> ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾</h6>'''
            
            
          card += f'''<h3 style="height: .0rem;">{hora}</h3>
          <h6 class="card-text" style="height: 0rem;">‾‾‾‾‾‾‾‾</h6>
          <img class="card-img-top" src="http://openweathermap.org/img/wn/{icone}@2x.png" alt="{descricaoGeral}" style="width: 10rem; height: 10rem;">
          <h5 style="height: 0rem;">{descricaoGeral}: {descricaoFiltrada}</h5>
          <h5 style="height: 0rem;">Umidade: {umidade}%</h5>
          <h5 style="height: 0rem;">Probabilidade de Precipitação: {probabilidadeDeChuva}%</h5>
          <h5 style="height: 0rem;">Vento: {ventoVelocidade} a {ventoAngulo}º</h5>
          <h6 style="height: 0rem;"></h6>'''

          # aqui fica o card
          sl.markdown(card, unsafe_allow_html=True)
          
          
          # sl.table(teste)
          
          descG = teste['Descrição']
          for feature in teste:
            descG[f'{dia}/{mes} {hora}'] = descricaoFiltrada
          
      else:
        'Não foi possível encontrar o resultado pesquisado'
        # sl.write(req) # mostra todo o arquivo JSON

  inicial()
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