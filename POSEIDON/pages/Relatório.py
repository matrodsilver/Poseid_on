import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import requests
import streamlit as sl
from datetime import date

dia = date.today()

cnv = canvas.Canvas(f'Relatorio_Poseid-ON.pdf', pagesize=A4)
cnv.setTitle(f'Relatorio {dia}')
cnv.setLineWidth(1)
cnv.drawCentredString(280, 800,f'Relatório Poseid-ON')
z=0
y = 0
Ytitulo = 760


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
  z= z+20
  dataBR = dados['feeds'][aux]['created_at']
  dia = dataBR[8:10]
  mes = dataBR[5:7]
  ano = dataBR[:4]
  if n ==1:
    cnv.drawString(30, 780, f'Esse foi o último valor pego dos sensores!')
  else:
    cnv.drawString(30, 780, f'Esses são os {n} últimos valores pegos dos sensores!')
  cnv.drawString(30, Ytitulo, "Data do dado coletado")
  cnv.drawString(180, Ytitulo, " Ultrassônico")
  cnv.drawString(285, Ytitulo, ' Infravermelho')
  cnv.drawString(383, Ytitulo, ' Infravermelho 2')
  cnv.drawString(495, Ytitulo, ' Água')
  cnv.line(20, 745-z, 550,745 - z)  # Ponto de início (50, A4[1] - 50) e ponto final (A4[0] - 50, 50
  hora = str(int(dataBR[11:13])-1) + dataBR[13:19]
  b = dados['feeds'][aux]['field2']
  c = dados['feeds'][aux]['field3']
  d = dados['feeds'][aux]['field4']
  e = dados['feeds'][aux]['field1']
  cnv.drawString(25,750-y, dataBR)
  cnv.drawString(200, 750- y, b)
  if c == 0.0 or 0:
    c = "Desligado"
  else:
    c = "Ligado"
  if d == 0.0 or 0:
    d = "Desligado"
  else:
    d = "Ligado"
  if e == 0.0 or 0:
    e = "Desligado"
  else:
    e = "Ligado"
  cnv.drawString(300, 750- y, c)
  cnv.drawString(400, 750- y, d)
  cnv.drawString(500, 750- y, e)
  print(b)
  print(c)
  print(d)
  print(e)
  print(dataBR)
  # if aux == 36:
  # descobrir como fazer uma segunda pagina  ----->, a cada 36 "linhas"
cnv.showPage()
cnv.save()
with open(f"Relatorio_Poseid-ON.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    if sl.download_button(
                          label='Baixe seu pdf aqui!!',
                          data=PDFbyte,
                          file_name=f'Relatorio_Poseid-ON.pdf',
                          mime='text/pdf',):
      sl.text(f'Download feito com sucesso!!')
