from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Laad games slechts 1 keer
with open('db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', games=db['games'])

@app.route('/api/games')
def api_games():
    return jsonify(db['games'])

@app.route('/api/games/<int:game_id>')
def get_game_by_id(game_id):
    game = next((g for g in db['games'] if g['id'] == game_id), None)
    return jsonify(game) if game else ('Game niet gevonden', 404)

if __name__ == '__main__':
    app.run(debug=True)
