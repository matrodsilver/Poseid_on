''' Código para envio de dados do clima e notificação sobre o volume da caixa '''

from pushbullet import Pushbullet # biblioteca para comunicação com o app de notificações
import requests # biblioteca para comunicação com links
import time # biblioteca para verificar a passagem do tempo

# # função que pega os valores do clima atual e o retorna
def pegarValores():
  urlTSultimoResultado = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results=1'

  resposta = requests.get(urlTSultimoResultado)

  if resposta.status_code == 200: # se conexão funcionou

    return resposta.json() # retornar arquivo json com os dados do clima
  
  else: # se não

    print('Erro na requisição')
    return {} # retorne erro


# função responsável por verificar volume da caixa retentora e notificar se necessário
def avisar():
  if int(pegarValores()['feeds'][0]['field1']) > 50:
    
    # usuários a serem notificados
    eu = 'o.9CYuBlpove3ErChfkLDjcmkNcjquJ1oz'
    tadashi = 'x'

    usuarios = [eu] # lista a ser percorrida com otodos os usuários
    
    for usuario in usuarios:
      pbt = Pushbullet(usuario)
      pbt.push_note(
          '⚠️Aviso⚠️', '⚠ O bueiro【𝟭】de São Paulo atingiu o limite de volume ⚠') # notificação


# função responsável por enviar informações do clima atual para o servidor
def enviar():
  token = '4127401294a510735af86031ebc9697b'
  # FIAP(lat, long) = -23.57323583564156, -46.623008521519246

  urlCurrent = f'https://api.openweathermap.org/data/2.5/weather?lat={-23.57323583564156}&lon={-46.623008521519246}&appid={token}&units=metric&lang={"pt_br"}'
  print(urlCurrent)
  reqCurrent = requests.get(urlCurrent)
  infoCurrent = reqCurrent.json()

  descricaoCurrent = infoCurrent['weather'][0]['description']
  mainCurrent = infoCurrent['weather'][0]['main']
  umidadeCurrent = infoCurrent['main']['humidity']
  chuva1h = 0 #infoCurrent['list'][0]['pop'] # não tem pop nem rain1h
  ventoVelocidadeCurrent = infoCurrent['wind']['speed']
  ventoAnguloCurrent = infoCurrent['wind']['deg']
  
  # icone = infoCurrent['weather'][0]['icon']

  requests.post(f"https://api.thingspeak.com/update?api_key=MB4W5VR14OISKTZU&field1='{descricaoCurrent}'&field2='{mainCurrent}'&field3={chuva1h}&field4={umidadeCurrent}&field5={ventoVelocidadeCurrent}&field6={ventoAnguloCurrent}&units=metric&lang={'pt_br'}")#&field7={None}&field8={None}")
  print(infoCurrent)


enviar()

while True:
  avisar()
  enviar()

  time.sleep(20)
