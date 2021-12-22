import json

data = json.load(open("C:/Users/beatr/Desktop/RASproj/Api.json"))



for item in data['Eventos']:
    print(item['Desporto'])


