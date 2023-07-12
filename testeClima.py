import requests as rq

token = '4127401294a510735af86031ebc9697b'

cidade = 'Osasco'
codigoDoPais = 'br'

urlA = f'http://api.openweathermap.org/data/2.5/weather?q={cidade},{codigoDoPais}&appid={token}&units=imperial&lang={"pt_br"}'
url5 = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade},{codigoDoPais}&appid={token}&units=imperial&lang={"pt_br"}'
url16 = f'http://api.openweathermap.org/data/2.5/forecast/daily?q={cidade},{codigoDoPais}&appid={token}&units=imperial&lang={"pt_br"}'

req = rq.get(url5)

info = req.json()

# print(info)

ultimoDia = 0

for n in range(0, len(info['list'])):
    tempo = info['list'][n]['weather'][0]
    vento = info['list'][n]['wind']
    data = info["list"][n]["dt_txt"]

    dia = data[8:10]
    mes = data[5:7]
    ano = data[0:4]
    hora = data[11:16]

    if dia != ultimoDia:
        print(f'__{dia}/{mes}/{ano}__\n--{hora}--')
        ultimoDia = dia
    else:
        print(f'--{hora}--')

    print(f'tempo {tempo["main"]} - {tempo["description"]}')
    print(f'Vento: {vento["speed"]} - {vento["deg"]}º\n')
