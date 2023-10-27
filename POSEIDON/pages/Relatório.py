from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import requests
import streamlit as sl
from datetime import date

dia = date.today().day

cnv = canvas.Canvas(f'Relatorio.pdf', pagesize=A4)
y = 0
Ytitulo = 800


sl.title('Faça o download do relatório')


try:
  n=int(sl.text_input(f'Quantidade dos últimos resultados a serem exibidos:'))
except:
  n = 15

def pegarValores(n):

  urlDados = f'https://api.thingspeak.com/channels/2127654/feeds.json?api_key=MZB0IDFGQR9AQVBW&results={n}'
  urlClima = f'https://api.thingspeak.com/channels/2244673/feeds.json?api_key=FOKGIHJ79MUZHIFW&results={n}'

  respostaDados = requests.get(urlDados)
  respostaClima = requests.get(urlClima)

  if respostaDados.status_code == 200:
    return [respostaDados.json(), respostaClima.json()]
  else:
    print('Erro na requisição')
    return {}


max = pegarValores(0)[1]['channel']['last_entry_id']
dados = pegarValores(n)[0]
clima = pegarValores(n)[1]


for aux in range(0, n):
  y = y+20
  dataBR = dados['feeds'][aux]['created_at']
  dia = dataBR[8:10]
  mes = dataBR[5:7]
  ano = dataBR[:4]
  cnv.drawString(25, Ytitulo, "Data do dado coletado")
  cnv.drawString(175, Ytitulo, " Ultrassonico")
  cnv.drawString(280, Ytitulo, ' Infravermelho')
  cnv.drawString(378, Ytitulo, ' Infravermelho 2')
  cnv.drawString(500, Ytitulo, ' Agua')
  hora = str(int(dataBR[11:13])-1) + dataBR[13:19]
  b = dados['feeds'][aux]['field2']
  c = dados['feeds'][aux]['field3']
  d = dados['feeds'][aux]['field4']
  e = dados['feeds'][aux]['field1']
  cnv.drawString(25,770-y, dataBR)
  cnv.drawString(200, 770- y, b)
  if c == 0.0 or 0:
    c = "desligado"
  else:
    c = "ligado"
  if d == 0.0 or 0:
    d = "desligado"
  else:
    d = "ligado"
  if e == 0.0 or 0:
    e = "desligado"
  else:
    e = "ligado"
  cnv.drawString(300, 770- y, c)
  cnv.drawString(400, 770- y, d)
  cnv.drawString(500, 770- y, e)
  print(b)
  print(c)
  print(d)
  print(e)
  print(dataBR)
  # if aux == 36:
  # descobrir como fazer uma segunda pagina  ----->, a cada 36 "linhas"
cnv.showPage()
cnv.save()
with open(f"Relatorio.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    if sl.download_button(
                          label='Baixe seu pdf aqui!!',
                          data=PDFbyte,
                          file_name=f'Relatorio.pdf',
                          mime='text/pdf',):
      sl.text('Download feito em {dia} com sucesso!!')
