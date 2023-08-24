from pushbullet import Pushbullet
import requests
import time


def pegarValores():
    url = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results=1'

    resposta = requests.get(url)

    if resposta.status_code == 200:
        return resposta.json()
    else:
        print('Erro na requisição')


eu = 'o.9CYuBlpove3ErChfkLDjcmkNcjquJ1oz'
tadashi = 'x'

usuarios = [eu]

while True:
    if int(pegarValores()['feeds'][0]['field1']) > 0:
        print('sin')
        for usuario in usuarios:
            pbt = Pushbullet(usuario)
            pbt.push_note('*o*', 'Bueiro em 300k%, ferrou parcero!')

    time.sleep(5)
