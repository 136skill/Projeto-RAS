import json

data = json.load(open("C:/Users/beatr/Desktop/RASCodigo/Api.json"))



for item in data['Eventos']:
    print(item['Minuto'])


