#para poder correr com python main.py em vez de usar as variaveis do flask
from projeto import app

if __name__ == '__main__':
    app.run(debug=True)