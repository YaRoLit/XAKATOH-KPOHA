from flask import Flask, render_template, request, jsonify
import index
from player import Player

app = Flask(__name__)

@app.route('/')
def index():
    username = "User"  # Замените на реальное имя пользователя
    items = tags # Днамический список с ключами и значениями
    return render_template('index.html', username=username, items=items)

@app.route('/auth', methods=['POST'])
def webapp():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    # Обработка данных пользователя
    return jsonify({"status": "success", "user_id": user_id, "username": username})

@app.route('/button-click/<key>', methods=['POST'])
def button_click(key):
    data = request.get_json()
    print(f"Button clicked: {data['key']}")
    return jsonify({"message": f"Button {data['key']} clicked!"})

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
