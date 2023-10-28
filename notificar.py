from pushbullet import Pushbullet
import requests
import time
import random


# esta função retorna o valor mais atual do banco de dados
def pegarValores():
  urlTSultimoResultado = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=<token>results=1'  # <token> é substituído pelo valor do token no código

  resposta = requests.get(urlTSultimoResultado)

  if resposta.status_code == 200:
    return resposta.json()
  else:
    print('Erro na requisição')
    return {}


# caso o valor mais atual do banco de dados seja maior que um volume determinado, esta função envia uma notificação de aviso ao pushbullet
def avisar():
  if float(pegarValores()['feeds'][0]['field2']) < 30:

    eu = '<token>'  # <token> é substituído pelo valor do token no código

    usuarios = [eu]

    for usuario in usuarios:
      pbt = Pushbullet(usuario)
      pbt.push_note(
          '⚠️Aviso⚠️', f'⚠ O bueiro【𝟭】de São Paulo atingiu o limite de volume ⚠\nAtualmente em: {57- float(pegarValores()["feeds"][0]["field2"])} cm')


# esta função envia os dados do clima atual para o banco de dados do clima
# juntamente com valores que simulam mais sistemas físicos Poseid-on
def enviar():
  token = '<token>'  # <token> é substituído pelo valor do token no código
  # FIAP -> lat, long = -23.57323583564156, -46.623008521519246

  urlCurrent = f'https://api.openweathermap.org/data/2.5/weather?lat={-23.57323583564156}&lon={-46.623008521519246}&appid={token}&units=metric&lang={"pt_br"}'
  print(urlCurrent)
  reqCurrent = requests.get(urlCurrent)
  infoCurrent = reqCurrent.json()

  # informações do clima requisitadas
  descricaoCurrent = infoCurrent['weather'][0]['description']
  mainCurrent = infoCurrent['weather'][0]['main']
  umidadeCurrent = infoCurrent['main']['humidity']
  ventoVelocidadeCurrent = infoCurrent['wind']['speed']
  ventoAnguloCurrent = infoCurrent['wind']['deg']

  # Simulação de valores de mais sistemas
  bueiro1 = round(random.uniform(0, 38),2)
  bueiro2 = round(random.uniform(0, 38),2)
  bueiro3 = round(random.uniform(0, 38),2)

  requests.post(
      f"https://api.thingspeak.com/update?api_key=<token>='{descricaoCurrent}'&field2='{mainCurrent}'&field3={0}&field4={umidadeCurrent}&field5={ventoVelocidadeCurrent}&field6={ventoAnguloCurrent}&units=metric&lang={'pt_br'}")  # envio do clima

  requests.post(
      f"https://api.thingspeak.com/update?api_key=S4NZJ1EOZ4SGHGWO&field1={bueiro1}&field2={bueiro2}&field3={bueiro3}&units=metric&lang={'pt_br'}")  # envio de dados simulados

  print(f'''__Valores atuais__
        Clima: {mainCurrent} ({descricaoCurrent})
        Umidade: {umidadeCurrent}
        Vento: {ventoVelocidadeCurrent} - {ventoAnguloCurrent}''')  # print para melhor vizualização dos dados


while True:
  avisar()
  enviar()

  time.sleep(20)
