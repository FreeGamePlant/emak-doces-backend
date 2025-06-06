from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CURTIDAS_FILE = 'curtidas.json'

def load_curtidas():
    if not os.path.exists(CURTIDAS_FILE):
        return {}
    with open(CURTIDAS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_curtidas(data):
    with open(CURTIDAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)

@app.route('/curtir', methods=['POST'])
def curtir():
    data = request.get_json()
    img = data.get('img')
    if not img:
        return jsonify({'error': 'Imagem não informada'}), 400
    curtidas = load_curtidas()
    curtidas[img] = curtidas.get(img, 0) + 1
    save_curtidas(curtidas)
    return jsonify({'ok': True, 'total': curtidas[img]})

@app.route('/curtidas', methods=['GET'])
def get_curtidas():
    curtidas = load_curtidas()
    return jsonify(curtidas)

@app.route('/descurtir', methods=['POST'])
def descurtir():
    data = request.get_json()
    img = data.get('img')
    if not img:
        return jsonify({'error': 'Imagem não informada'}), 400
    curtidas = load_curtidas()
    if curtidas.get(img, 0) > 0:
        curtidas[img] -= 1
    save_curtidas(curtidas)
    return jsonify({'ok': True, 'total': curtidas[img]})

if __name__ == '__main__':
    app.run(debug=True)