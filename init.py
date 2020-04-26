import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, abort
from flask_cors import cross_origin,CORS

app = Flask(__name__)
CORS(app)

URL = "http://200.46.245.230:8080/PortalCAE-WAR-MODULE/SesionPortalServlet?accion=6&NumDistribuidor=99&NomUsuario=usuInternet&NomHost=AFT&NomDominio=aft.cl&Trx=&RutUsuario=0&NumTarjeta={}&bloqueable="


@app.route('/')
def init():
    data = {
        'Description':'Ingresa el número de la tarjeta para obtener el balance',
        'URL':'/api/v2/search/<cardID>'
    }
    return jsonify(data)

@app.route('/api/v2/search/<string:cardID>', methods=['GET'])
def getBalance(cardID):
    res = requests.get(URL.format(cardID))
    try:
        if (res.status_code == 200 and res.ok):
            print('Ok')
            soup = BeautifulSoup(res.content, 'html.parser')
            result = soup.find('table', cellspacing='1')
            td = result.find_all('td', class_='verdanabold-ckc')
            if len(td) > 2:
                data = {
                    'Success': 1,
                    'Item': {
                        'CardID': td[1].text,
                        'Status': td[3].text,
                        'Balance': td[5].text,
                        'LastTransactionAt': td[7].text
                    }
                }
            else:
                abort(500)
    except Exception as e:
        abort(404)
    return jsonify(data)


@app.errorhandler(404)
def not_found(error):
    data = {
        'Success': -1,
        'Item': {
            'Description': 'Error 404.',
            'Message': 'Not Found',
            'Error': str(error)
        }
    }
    return jsonify(data)

@app.errorhandler(500)
def internal_error(error):
    data = {
        'Success': -1,
        'Item': {
            'Description': 'Error 500.',
            'Message': 'Internal Server Error',
            'Error': str(error)
        }
    }
    return jsonify(data)

@app.errorhandler(405)
def method_not_allowed(error):
    data = {
        'Success': -1,
        'Item': {
            'Description': 'Error 405.',
            'Messaje':'Method Not Allowed',
            'Error': str(error)
        }
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False, port=5000)
