import requests
import streamlit as sl


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

      dados = pegarValores(n)

    except:
      n = 15
      
      dados = pegarValores(n)

      sl.markdown(f'''<h6 style ="height: 0rem; color: #808080; ">Digite um número de 1 a {max}</h6>
                  <h6 style ="height: 0rem; color: #808080; ">Exibindo os 15 resultados mais recentes</h6>''', unsafe_allow_html=True)

    # teste condicional de funcionamento
    if dados is not None:

      bd = []
      horario = []
      horarioMin = []

      tabGrafico, tabDados = sl.tabs(["Gráfico", "Dados"])
      for numero in range(0, n):  # type: ignore

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

          # visibilidade =
          # nuvens =

          dia = data[8:10]
          mes = data[5:7]
          ano = data[0:4]
          hora = data[11:16]

          def cor(prob):
            prob = round(prob * 100)
            prob2 = round(99 - prob)

            if prob > 99:
              prob = 99
            if prob2 < 0:
              prob2 = 0

            if len(str(prob)) < 2:
              add = ''

              while len(str(add)) < 2 - len(str(prob)):
                add += '0'

              add += f'{prob}'

              prob = add

            if len(str(prob2)) < 2:
              add = ''

              while len(str(add)) < 2 - len(str(prob2)):
                add += '0'

              add += f'{prob2}'

              prob2 = add

            hex = f'#{prob}{prob2}00'

            return hex

          def recomendar():
            if probabilidadeDeChuva > .98:
              return '(Chuva é certa, coleta não é recomendada)'
            else:
              return ''

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
          <h5 style="height: 0rem;">Probabilidade de Precipitação: <span style="height: 0rem; color: {cor(probabilidadeDeChuva)}">{round(probabilidadeDeChuva * 100)}% {recomendar()}</span></h5>
          <h5 style="height: 0rem;">Vento: {ventoVelocidade} a {ventoAngulo}º</h5>
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
