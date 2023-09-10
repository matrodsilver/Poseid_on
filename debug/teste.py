# import requests
# import pandas as p
# import streamlit as sl
# import pandas as pd
# import streamlit as st

# data = {'29/04 16:42:23': 0, '29/04 17:21:07': 0, '14/05 04:45:48': 0, '14/05 06:24:14': 2.0, '14/05 06:24:39': 7.0, '14/05 06:25:09': 2.0, '14/05 06:25:24': 5.0, '14/05 06:25:40': 7.0, '14/05 06:25:56': 5.0, '15/05 21:38:50': 7.0, '15/05 21:39:05': 5.0, '15/05 21:39:20': 3.0, '15/05 21:39:37': 2.0, '15/05 21:39:54': 8.0, '15/05 21:40:09': 1.0, '15/05 21:40:24': 7.0, '15/05 21:40:40': 3.0, '15/05 21:40:55': 8.0, '15/05 21:41:10': 2.0, '17/05 18:31:47': 0, '17/05 18:32:31': 0, '17/05 18:33:14': 0, '17/05 18:33:31': 0, '17/05 18:34:07': 0, '17/05 18:34:38': 0, '17/05 18:34:56': 0, '17/05 18:35:12': 0, '17/05 18:35:28': 0, '17/05 18:36:35': 0, '17/05 18:36:56': 0, '17/05 18:37:13': 0, '17/05 18:37:43': 0, '17/05 18:37:59': 0, '17/05 18:38:16': 0, '17/05 18:38:32': 0, '17/05 18:38:53': 0, '17/05 18:39:12': 0, '17/05 18:39:32': 0, '17/05 18:39:48': 0, '17/05 18:40:04': 0, '17/05 18:40:23': 0, '17/05 18:40:50': 0, '17/05 18:41:16': 0, '17/05 18:41:39': 0, '17/05 18:41:54': 0, '17/05 18:42:11': 0, '17/05 18:42:28': 0, '17/05 18:42:48': 0, '17/05 18:44:18': 0, '17/05 18:44:39': 0, '17/05 18:45:25': 0, '17/05 18:45:41': 0, '17/05 18:46:00': 0, '17/05 18:46:16': 0, '17/05 18:46:39': 0, '17/05 18:47:00': 0, '17/05 19:23:24': 0, '28/06 23:53:01': 0, '10/08 20:09:01': 0, '10/08 20:42:03': 0, '10/08 20:42:23': 0, '10/08 20:42:56': 0, '10/08 20:43:16': 0, '10/08 20:43:36': 0, '10/08 20:43:57': 0, '10/08 20:44:17': 0, '10/08 20:44:37': 0, '10/08 20:45:17': 0, '10/08 20:45:38': 0, '10/08 20:45:58': 0, '10/08 20:46:18': 0, '10/08 20:46:39': 0, '18/08 01:56:18': 109.3, '18/08 01:56:40': 0, '21/08 23:51:09': 0, '21/08 23:51:31': 0, '27/08 08:28:08': 0, '27/08 08:28:37': 19.29, '27/08 08:28:58': 0, '27/08 08:29:18': 0, '27/08 08:29:38': 0, '27/08 08:29:59': 0, '27/08 08:30:19': 0, '27/08 08:30:39': 0, '27/08 08:31:00': 0, '27/08 08:33:35': 0, '27/08 08:33:55': 180.37, '27/08 08:34:16': 81.12, '27/08 08:34:35': 83.59, '27/08 08:34:55': 35.57, '27/08 08:35:16': 298.79, '28/08 03:52:26': 0, '28/08 03:52:47': 0, '28/08 03:53:07': 0, '28/08 03:53:27': 0, '28/08 03:53:49': 0, '28/08 03:54:09': 0, '28/08 03:54:29': 0, '28/08 03:54:49': 0, '28/08 03:55:10': 0, '28/08 03:55:30': 0, '28/08 03:55:50': 0, '28/08 03:56:11': 0, '28/08 03:56:31': 0, '28/08 03:56:51': 0, '28/08 03:57:11': 0, '28/08 03:57:32': 0, '28/08 03:57:52': 0, '28/08 03:58:13': 0, '28/08 03:58:34': 0, '28/08 04:22:52': 86.3, '28/08 04:23:12': 88.08, '28/08 04:23:32': 63.11, '28/08 04:23:52': 75.01, '28/08 04:24:13': 19.29, '28/08 04:24:33': 77.26, '28/08 04:24:53': 58.64, '28/08 04:25:13': 42.77, '28/08 04:25:34': 98.34, '28/08 04:25:54': 97.98, '28/08 04:26:14': 98.36, '28/08 04:26:35': 89.78, '28/08 04:26:55': 87.62, '28/08 04:45:17': 99.23, '28/08 04:45:38': 76.73, '28/08 04:50:34': 51.48, '28/08 04:50:55': 51.45, '28/08 04:51:15': 19.28, '28/08 04:51:38': 42.77, '28/08 10:37:41': 75.56, '28/08 10:38:03': 19.16, '28/08 10:38:25': 42.63, '28/08 10:38:46': 42.65, '28/08 11:55:16': 44.76, '28/08 11:55:39': 43.9, '28/08 11:55:59': 43.9, '28/08 11:56:21': 43.92, '28/08 11:56:42': 43.9, '28/08 11:57:03': 44.85, '28/08 11:57:23': 44.85, '28/08 11:57:44': 44.86, '28/08 11:58:06': 45.22, '28/08 11:58:25': 44.86, '28/08 11:58:48': 45.24, '28/08 11:59:08': 44.83, '28/08 11:59:29': 44.81, '28/08 11:59:51': 45.21, '28/08 12:00:12': 44.76, '28/08 12:00:32': 44.28, '28/08 12:00:55': 44.78, '28/08 12:01:16': 44.78, '28/08 12:01:36': 44.68, '28/08 12:01:57': 44.68, '28/08 12:02:19': 44.66, '28/08 12:02:41': 44.66, '28/08 12:03:02': 43.87,
#         '28/08 12:03:23': 44.26, '28/08 12:03:44': 43.85, '28/08 12:04:05': 44.26, '28/08 12:04:26': 43.85, '28/08 12:04:48': 43.87, '28/08 12:05:08': 43.84, '28/08 12:05:30': 43.49, '28/08 12:05:52': 43.87, '28/08 12:06:13': 43.85, '28/08 12:06:34': 43.94, '28/08 12:06:56': 44.26, '28/08 12:07:17': 43.89, '28/08 12:07:38': 43.85, '28/08 12:08:00': 42.7, '28/08 12:08:21': 42.69, '28/08 12:08:42': 43.1, '28/08 12:09:04': 43.08, '28/08 12:09:25': 52.19, '28/08 12:09:46': 59.6, '28/08 12:10:05': 59.99, '28/08 14:42:42': 54.35, '28/08 14:43:03': 54.35, '28/08 14:43:25': 53.92, '28/08 14:43:46': 53.32, '28/08 14:44:05': 45.02, '28/08 14:44:26': 52.89, '28/08 14:44:48': 0, '28/08 14:45:11': 54.33, '28/08 14:45:32': 42.72, '28/08 14:45:53': 42.69, '28/08 14:46:14': 42.81, '28/08 14:46:35': 43.22, '28/08 14:46:56': 43.2, '28/08 14:47:17': 43.24, '28/08 14:47:38': 43.22, '28/08 14:48:00': 43.22, '28/08 14:48:21': 43.24, '28/08 14:48:43': 43.2, '28/08 14:49:04': 43.22, '28/08 14:49:25': 43.22, '28/08 14:49:47': 43.22, '28/08 14:50:06': 53.04, '28/08 14:50:27': 43.66, '28/08 14:50:48': 43.12, '28/08 14:51:09': 0, '28/08 14:51:29': 44.09, '28/08 14:51:51': 43.97, '01/09 12:40:58': 0, '01/09 12:41:23': 0, '01/09 12:41:45': 0, '01/09 12:42:08': 175.24, '01/09 12:42:30': 170.63, '01/09 12:42:52': 19.21, '01/09 12:43:19': 21.64, '01/09 12:43:41': 105.87, '01/09 12:44:03': 68.36, '01/09 12:44:26': 86.09, '02/09 15:59:22': 192.63, '02/09 16:00:48': 192.92, '02/09 16:01:09': 198.97, '02/09 16:01:38': 199.56, '02/09 16:02:02': 191.65, '02/09 16:02:27': 192.42, '02/09 16:03:32': 0, '02/09 16:04:23': 0, '02/09 16:05:00': 0, '02/09 16:05:23': 189.01, '02/09 16:05:49': 201.02, '03/09 02:52:17': 0, '03/09 02:52:44': 0, '03/09 02:53:09': 47.23, '03/09 02:53:30': 45.34, '03/09 02:53:46': 45.77, '03/09 02:54:08': 133.41, '03/09 02:54:30': 162.48, '03/09 02:55:06': 19.48, '03/09 02:55:27': 21.95, '03/09 02:55:48': 19.33, '03/09 02:56:09': 22.78, '03/09 02:56:29': 22.69, '03/09 02:56:50': 21.04, '03/09 02:57:10': 19.31, '03/09 02:57:31': 19.19, '03/09 02:58:07': 19.35, '03/09 02:58:28': 19.19, '03/09 02:59:19': 22.3, '03/09 02:59:40': 21.8, '03/09 03:00:00': 21.85, '03/09 03:00:21': 19.45, '03/09 03:00:42': 19.59, '03/09 03:01:02': 19.29, '03/09 03:01:23': 53.53, '03/09 03:01:44': 54.4, '03/09 03:02:05': 42.53, '03/09 03:02:26': 51.35, '03/09 03:02:47': 55.33, '03/09 03:03:08': 19.41, '03/09 03:03:29': 55.5, '03/09 03:03:50': 39.82, '03/09 03:04:11': 38.19, '03/09 03:04:32': 31.81, '03/09 03:04:53': 44.88, '03/09 03:05:13': 55.62, '03/09 03:05:35': 36.53, '03/09 03:05:55': 55.57, '03/09 03:06:17': 19.23, '03/09 03:06:37': 45.07, '03/09 03:06:58': 19.19, '03/09 03:07:19': 19.47, '03/09 03:07:40': 27.71, '03/09 03:08:00': 19.43, '03/09 03:08:21': 25.98, '03/09 03:08:41': 24.37, '03/09 03:10:02': 17.51, '03/09 03:10:19': 17.92, '03/09 03:10:39': 13.94, '03/09 03:11:00': 5.35, '03/09 03:11:20': 2.97, '03/09 03:11:41': 2.97, '03/09 03:12:01': 2.97, '03/09 03:12:22': 2.97, '03/09 03:12:43': 19.53, '03/09 03:13:19': 14.01, '03/09 03:13:55': 78.8, '03/09 03:14:47': 44.76, '03/09 03:15:08': 45.45, '03/09 03:15:29': 66.08, '03/09 03:16:20': 48.41, '03/09 03:16:56': 3.57, '03/09 03:17:47': 3.91, '03/09 03:18:08': 3.91, '03/09 03:18:28': 3.91, '03/09 03:18:49': 3.91, '03/09 03:19:09': 3.91, '03/09 03:19:29': 3.91, '03/09 03:19:50': 3.91, '03/09 03:20:10': 3.91, '03/09 03:20:31': 3.91, '03/09 03:21:22': 42.02, '03/09 03:21:42': 14.85, '03/09 03:50:32': 0, '03/09 03:51:27': 19.19, '03/09 03:52:04': 19.47}
# dates_with_year = [d.replace(' ', '/2023 ') for d in data.keys()]

# df = pd.DataFrame({
#     'x': dates_with_year,
#     'y': data.values()
# })

# df['x'] = pd.to_datetime(df['x'])
# df = df.sort_values(by='x')

# st.line_chart(
#     df,
#     x='x',
#     y='y',
# )
################
# código no site

# def pegarValores(n):

#   url = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'

#   resposta = requests.get(url)
#   if resposta.status_code == 200:
#     return resposta.json()
#   else:
#     print('Erro na requisição')
#     return {}


# dados = pegarValores(299)

# inteiro = False
# if dados is not None:

#   bd = []
#   horario = []
#   horarioMin = []

#   tabGrafico, tabDados = sl.tabs(["Gráfico", "Dados"])
#   for numero in range(0, n):  # type: ignore

#     dataBR = dados['feeds'][numero]['created_at']

#     dia = dataBR[8:10]
#     mes = dataBR[5:7]
#     ano = dataBR[:4]
#     hora = dataBR[11:19]

#     horario.append(f'{dia}/{mes}/{ano} {hora}')
#     horarioMin.append(f'{dia}/{mes} {hora}')

#     # opção 1
#     try:
#       if float(dados['feeds'][numero]['field2']) > 0:
#         bd.append(float(dados['feeds'][numero]['field2']))
#       else:
#         bd.append(0)

#     except:
#       bd.append(0)

#     # # opção 2
#     # try:
#     #   if float(dados['feeds'][numero]['field2']) > 0:
#     #     bd.append(float(dados['feeds'][numero]['field2']))

#     #   else: #(implícito na lógica)
#     #   # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
#     #     pass

#     # except:
#     # # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
#     #   pass

#   dicionarioDados = {}
#   dicionarioDadosMin = {}
#   for n in range(0, len(bd)):
#     dicionarioDados[str(horario[n])] = bd[n]
#     dicionarioDadosMin[str(horarioMin[n])] = bd[n]

#   datas = [d.replace(' ', '/2023 ') for d in dicionarioDadosMin.keys()]

#   df = p.DataFrame({
#       'x': datas,
#       'y': dicionarioDadosMin.values()
#   })

#   df['x'] = p.to_datetime(df['x']).dt.strftime('%d/%m %H:%M:%S')
#   df = df.sort_values(by='x')

#   # sl.line_chart(
#   #     df,
#   #     x='x',
#   #     y='y',
#   # )

#   with tabGrafico:
#     sl.line_chart(df, x='x', y='y',)

#   with tabDados:
#     sl.table(dicionarioDados)
###############################
#  teste

# n = 12345678

# if len(str(n)) < 7:
#   add = ''
  
#   while len(str(add)) < 7 - len(str(n)):
#     add += '0'
  
#   add += f'{n}'
#   print(f'add: {add}\nn  : {n}')
  
# print('pronto')
#################
# implementado

# import requests
# import streamlit as sl
# import pandas as p


# def pegarValores(n):

#   url = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'

#   resposta = requests.get(url)
#   if resposta.status_code == 200:
#     return resposta.json()
#   else:
#     print('Erro na requisição')
#     return {}


# sl.sidebar.title('Menu')
# paginaSelecionada = sl.sidebar.selectbox(
#     'Selecione a página a ser exibida', ['Verificação', 'Dicas'])


# if paginaSelecionada == 'Verificação':
#   def inicial():
#     pegarValores(15)

#   def interface():
#     ## Teste Site ##
#     dados = None
#     max = pegarValores(0)['channel']['last_entry_id']

#     sl.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">', unsafe_allow_html=True)
#     sl.title('Consulte aqui as informaões necessárias')

#     n = sl.text_input(
#         f'Quantidade dos últimos resultados a serem exibidos:')

#     try:
#       n = int(n)

#       if n > max or n < 1:
#         raise Exception('Número fora de alcance')

#       inteiro = True
#       dados = pegarValores(n)

#     except:
#       f'Digite um número de 1 a {max}'

#       inteiro = False

#     # teste condicional de funcionamento
#     # type: ignore
#     if sl.button('Verificar') and inteiro and (0 < n <= dados['channel']['last_entry_id']): #type: ignore

#       if dados is not None:

#         bd = []
#         horario = []
#         horarioMin = []
#         index = 0

#         tabGrafico, tabDados = sl.tabs(["Gráfico", "Dados"])

#         for numero in range(n):  # type: ignore

#           dataBR = dados['feeds'][numero]['created_at']
          
#           dia = dataBR[8:10]
#           mes = dataBR[5:7]
#           ano = dataBR[:4]
#           hora = dataBR[11:19]

#           index += 1
#           if len(str(index)) < 7:
#             add = ''

#             while len(str(add)) < 7 - len(str(index)):
#               add += '0'

#             add += f'{index}'

#             horario.append(f'{add}-{dia}/{mes}/{ano} {hora}')
#             horarioMin.append(f'{add}-{dia}/{mes} {hora}')

#             f"{add}; {add}-{dia}/{mes}/{ano} {hora}; {dataBR}"

#           # opção 1
#           try:
#             if float(dados['feeds'][numero]['field2']) > 0:
#               bd.append(float(dados['feeds'][numero]['field2']))
#             else:
#               bd.append(0)

#           except:
#             bd.append(0)

#           # # opção 2
#           # try:
#           #   if float(dados['feeds'][numero]['field2']) > 0:
#           #     bd.append(float(dados['feeds'][numero]['field2']))

#           #   else: #(implícito na lógica)
#           #   # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
#           #     pass

#           # except:
#           # # desconsidera medidas menores que 0, já que devem ser erros (no código final, mudar para "menor que a distância mínima detectável do sensor que a gente tá usando")
#           #   pass

#         dicionarioDados = {}
#         dicionarioDadosMin = {}
#         for n in range(len(bd)):
#           dicionarioDados[str(horario[n])] = bd[n]
#           dicionarioDadosMin[str(horarioMin[n])] = bd[n]
          
#         f'{dicionarioDadosMin}'

#         with tabGrafico:
#           sl.line_chart(dicionarioDadosMin)

#         with tabDados:
#           sl.table(dicionarioDados)

#         # sl.write(dados)

#     ## Teste Clima##
#     token = '4127401294a510735af86031ebc9697b'

#     cidade = sl.text_input(
#         'Digite a cidade a qual deseja consultar informações climáticas:')
#     codigoDoPais = 'BR'

#     url5 = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=metric&lang={"pt_br"}'

#     req = requests.get(url5)

#     if sl.button('Consultar'):
#       if req.status_code == 200:

#         info = req.json()

#         # ultimoDia = 0

#         for n in range(len(info['list'])):
#           tempo = info['list'][n]['weather'][0]
#           vento = info['list'][n]['wind']
#           data = info["list"][n]["dt_txt"]

#           dia = data[8:10]
#           mes = data[5:7]
#           ano = data[0:4]
#           hora = data[11:16]

#           # aqui fica o card
#           sl.markdown(f'''
#                             <div class="card" style="width: 10rem;">
#                                 <img class="card-img-top" src="http://openweathermap.org/img/wn/{tempo["icon"]}@2x.png" alt="{tempo["main"]}">
#                                 <div class="card-body">
#                                     <h3 class="card-title">{tempo["main"]} - {tempo["description"]}</h3>
#                                     <h4 class="card-text">_{dia}/{mes}/{ano}_</h4>
#                                     <h4>--{hora}--</h4>
#                                     <h5>Vento: {vento["speed"]} - {vento["deg"]}º</h5>
#                                 </div>
#                             </div>
#                         ''', unsafe_allow_html=True)
#           # sl.write(info)

#       else:
#         'Não foi possível encontrar o resultado pesquisado'
#         # sl.write(req) # mostra todo o arquivo JSON

#   interface()

# elif paginaSelecionada == 'Dicas':
#   sl.markdown('''
# <h3>Preserve o Nosso Meio Ambiente: Não Jogue Lixo na Rua ou nos Bueiros</h3>

# Em nosso dia a dia agitado, muitas vezes, esquecemos o impacto que nossas ações podem ter no meio ambiente. Uma dessas ações é o descarte inadequado de lixo, especialmente nas ruas e bueiros. Parece inofensivo, mas o que você joga na rua ou nos bueiros tem consequências sérias para o nosso planeta e para a qualidade de vida de todos nós.

# 1. Poluição Ambiental: Quando jogamos lixo na rua, ele não desaparece magicamente. Em vez disso, é carregado pela chuva para os bueiros e, eventualmente, para os rios e oceanos. Isso polui nossos preciosos recursos hídricos e ameaça a vida marinha.

# 2. Inundações: Os bueiros entupidos com lixo podem obstruir o fluxo de água da chuva. Isso aumenta o risco de inundações, causando danos materiais e colocando vidas em perigo.

# 3. Saúde Pública: Lixo nas ruas atrai pragas, cria condições insalubres e aumenta o risco de doenças. Ninguém quer viver em um ambiente sujo e doente.

# 4. Beleza Natural e Estética: Jogue lixo na rua e você estará contribuindo para a degradação da beleza natural de sua cidade. Lixeiras e contentores de reciclagem estão amplamente disponíveis para manter nossas ruas limpas e agradáveis.

# 5. Responsabilidade Coletiva: Preservar o meio ambiente não é apenas responsabilidade do governo ou de organizações ambientais. Cada um de nós tem um papel a desempenhar. Pequenas ações individuais podem criar um grande impacto positivo quando se trata de manter nosso planeta saudável.

# <h4>E então o que você pode fazer?</h4>
# <ul>
#     <li>
#         Descarte Responsável: Sempre leve seu lixo até uma lixeira adequada ou contentor de reciclagem. Ensine as crianças desde cedo a fazer o mesmo.
#     </li>
#     <li>
#         Recicle: Separe seu lixo reciclável do lixo comum. A reciclagem ajuda a reduzir a quantidade de lixo que vai parar nos aterros sanitários.
#     </li>
#     <li>
#         Participe de Campanhas de Limpeza: Una-se a grupos locais que realizam limpezas regulares em sua comunidade. É uma maneira eficaz de fazer a diferença.
#     </li>
#     <li>
#         Eduque os Outros: Compartilhe informações sobre a importância de não jogar lixo na rua e nos bueiros com amigos e familiares. Quanto mais pessoas estiverem cientes, maior será o impacto positivo.
#     </li>
# </ul>

# <h6>Cada ação conta. Vamos trabalhar juntos para manter nossas ruas limpas, nossos bueiros desobstruídos e nosso planeta saudável para as futuras gerações. A mudança começa com você!</h6>
# ''', unsafe_allow_html=True)
##############################
# EX DataBase Utilizável

# teste = {'Descrição': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
#                    'Generalizado': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
                   
#                    'Visualização': {'data1':1, 'data2': 2, 'data3': 3, 'data4': 4}, # debug
                   
#                    'Umidade': {'data1':f'{1}%','data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
#                    'Probabilidade de Chuva': {'data1':f'{1}%', 'data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
#                    'Vento Velocidade': {'data1':f'{1}km/h', 'data2': f'{2}km/h', 'data3': f'{3}km/h', 'data4': f'{4}km/h'},
#                    'Vento Angulo': {'data1':f'{1}º', 'data2': f'{2}º', 'data3': f'{3}º', 'data4': f'{4}º'}} # debug
###################################################################################################################
#  markdowns

import streamlit as sl
# import requests
# from IPython.display import display, HTML

# html_content = """
# <img src="https://pbs.twimg.com/profile_images/1337904011920494594/QtqyB40m_400x400.jpg">
# """

# # Display the HTML content
# display(HTML(html_content))

# sl.markdown(f'''**Streamlit** ***is*** **really**
#             <h2 class="card-text">_***{'1'}/{'2'}/{'3'}***_</h2>
#             ***cool***.''')
# sl.markdown('''
#     :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in] :grey[pretty] :rainbow[colors].''')
# sl.markdown("Here's a bouquet &mdash;\
#             :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

# sl.markdown('''If you end a line with two spaces,
# a soft return is used for the next line.

# Two (or more) newline characters in a row will result in a hard return.

# alo

# <div class="card" style="width: 10rem;">
#       <img class="card-img-top" src="http://openweathermap.org/img/wn/{req5.json()['list'][0]['weather'][0]['icon']}@2x.png" alt="">
#   </div>
#               ''')
# sl.markdown(f'''
#                   <div class="card" style="width: 20rem; height: 0rem;">
#                       <img class="card-img-top" src="http://openweathermap.org/img/wn/{requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q=Osasco,BR&appid=4127401294a510735af86031ebc9697b&units=metric&lang=pt_br').json()['list'][0]['weather'][0]['icon']}@2x.png" alt="">
#                       <div class="card-body">
#                           <h3 class="card-title"> - </h3>
#                           <h4 class="card-text">__</h4>
#                           <h4>--</h4>
#                           <h5>Vento: º</h5>
#                           <h5>Umidade: %</h5>
#                           <h5>Probabilidade de Chuva: %</h5>
#                           <h5>teste: %</h5>
#                           </div>
#                   </div>
#               ''', unsafe_allow_html=True)

# opção 2
# f'''
# <div class="card" style="width: 20rem;">
#     <img class="card-img-top" src="http://openweathermap.org/img/wn/{icone}@2x.png" alt="{descricaoGeral}">
#     <div class="card-body">
#         <h3 class="card-text">_{dia}/{mes}/{ano}_</h3>
#         <h3>-{hora}-</h3>
#         <h4>{descricaoGeral}: {descricaoFiltrada}</h4>
#         <h5>Umidade: {umidade}%</h5>
#         <h5>Probabilidade de Chuva: {probabilidadeDeChuva}%</h5>
#         <h5>Vento: {ventoVelocidade} a {ventoAngulo}º</h5>
#         </div>
# </div>
# '''

teste = {'Descrição': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
                   'Filtrada': {'data1':f'{"a"}', 'data2': f'{"b"}', 'data3': f'{"c"}', 'data4': f'{"d"}'},
                   
                   'Visualização': {'data1':1, 'data2': 2, 'data3': 3, 'data4': 4}, # debug
                   
                   'Umidade': {'data1':f'{1}%','data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
                   'Probabilidade de Chuva': {'data1':f'{1}%', 'data2': f'{2}%', 'data3': f'{3}%', 'data4': f'{4}%'},
                   'Vento Velocidade': {'data1':f'{1}km/h', 'data2': f'{2}km/h', 'data3': f'{3}km/h', 'data4': f'{4}km/h'},
                   'Vento Angulo': {'data1':f'{1}º', 'data2': f'{2}º', 'data3': f'{3}º', 'data4': f'{4}º'}} # debug

sl.table(teste)
##########################
# várias linhas no gráfico

import streamlit as sl
import pandas as p
import numpy as np

chart_data = p.DataFrame(np.random.rand(10, 4), columns= ["NO2","C2H5CH","VOC","CO"])

sl.line_chart(chart_data)
sl.area_chart(chart_data)
