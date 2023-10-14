from pushbullet import Pushbullet
import requests
import time


def pegarValores():
  urlTSultimoResultado = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results=1'

  resposta = requests.get(urlTSultimoResultado)

  if resposta.status_code == 200:
    return resposta.json()
  else:
    print('Erro na requisição')
    return {}


def avisar():
  if float(pegarValores()['feeds'][0]['field2']) < 30:
    
    eu = 'o.9CYuBlpove3ErChfkLDjcmkNcjquJ1oz'
    tadashi = 'x'

    usuarios = [eu]
    
    for usuario in usuarios:  # type:ignore
      pbt = Pushbullet(usuario)
      pbt.push_note(
          '⚠️Aviso⚠️', f'⚠ O bueiro【𝟭】de São Paulo atingiu o limite de volume ⚠\nAtualmente em: {float(pegarValores()["feeds"][0]["field2"])} cm')


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
  chuva1h = 0 #infoCurrent['list'][0]['pop'] #  pop / rain1h
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
