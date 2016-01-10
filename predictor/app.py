import os
from json import dumps
from flask import Flask, render_template, request

from data import get_data

STATIC = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
app = Flask(__name__, static_folder=STATIC, static_url_path='')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/probability")
def probability():
    game_id = request.args.get('game_id')
    if game_id is None:
        return "Give me a game id..."
    return render_template('probability.html', game_id=game_id)


@app.route("/data", methods=['POST'])
def data():
    game_id = request.json.get('game_id')
    pbp_data = get_data(game_id)
    return dumps(list(pbp_data))


if __name__ == '__main__':
    app.run()
