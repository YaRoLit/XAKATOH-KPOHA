from flask import Flask, render_template, request, jsonify
from player import Player

app = Flask(__name__)

@app.route('/')
def index():
    username = "User"  # Замените на реальное имя пользователя
    items = {
        "Ключ 1": "Значение 1",
        "Ключ 2": "Значение 2",
        "Ключ 3": "Значение 3",
        "Клюdч 1": "Значение 1",
        "Ключd 2": "Значение 2",
        "Ключv 3": "Значение 3",
        "Ключv 1": "Значение 1",
        "Клю ч 2": "Значение 2",
        "Ключ 3": "Значение 3",
        "Ключz 1": "Значение 1",
        "Клюxч 2": "Значение 2",
        "Ключf 3": "Значение 3",
        "Ключf 1": "Значение 1",
        "Ключ e2": "Значение 2",
        "Ключ 3q": "Значение 3",
        "gКлюч 1": "Значение 1",
        "Кvлюч 2": "Значение 2",
        "Клwюч 3": "Значение 3",
        "Клюyч 1": "Значение 1",
        "Ключw 2": "Значение 2",
        "Ключ j3": "Значение 3",
        "Ключ 1a": "Значение 1",
        "gКлюч 2": "Значение 2",
        "Кsлюч 3": "Значение 3"
    }  # Днамический список с ключами и значениями
    return render_template('index.html', username=username, items=items)

@app.route('/button-click/<key>', methods=['POST'])
def button_click(key):
    data = request.get_json()
    print(f"Button clicked: {data['key']}")
    return jsonify({"message": f"Button {data['key']} clicked!"})

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
