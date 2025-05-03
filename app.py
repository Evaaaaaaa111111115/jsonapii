# bronnen:https://www.w3schools.com/js/js_json_intro.asp
# https://www.w3schools.com/html/
# https://www.w3schools.com/css/
# https://github.com/topics/flask
# chat gpt
# https://realpython.com/tutorials/flask/
# voor deze opdracht heb ik ook Zinedine geraadpleegd
# https://www.youtube.com/watch?v=Z1RJmh_OqeA&ab_channel=TraversyMedia
# debugging met print statements : chat gpt
# doorsturen naar github gef fouten: chatgpt

from flask import Flask, jsonify, render_template
import requests
import json



app = Flask(__name__)


API_URL = "https://my-json-server.typicode.com/Evaaaaaaa111111115/jsonapii"

games = requests.get(f"{API_URL}/games").json()
platforms = requests.get(f"{API_URL}/platforms").json()


@app.route('/')
def home():
    games = requests.get(f"{API_URL}/games").json()
    platforms_response = requests.get(f"{API_URL}/platforms")
    print("DEBUG: Platform API response:", platforms_response.text)

    try:
        platforms = platforms_response.json()
    except ValueError:
        return "Fout bij laden platforms: geen geldige JSON."

    # Print om te controleren of de structuur klopt
    print("DEBUG: platforms:", platforms)

    try:
        platform_dict = {p['id']: p['naam'] for p in platforms}
    except KeyError as e:
        return f"KeyError: {e} – Controleer of elk platform een 'id' en 'naam' heeft."

    for game in games:
        game['platform'] = platform_dict.get(game['platform_id'], 'Onbekend')

    return render_template(
        'index.html',
        games=games,
        platforms=platforms,
        platform_dict=platform_dict
    )


    #  games = requests.get(f"{API_URL}/games").json()
    #  return render_template('index.html', games=games)
    # # return render_template('index.html', games=db['games'])

@app.route('/api/games')
def api_games():
    response = requests.get(f"{API_URL}/games")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Games konden niet worden opgehaald"}), 500
        
    # return jsonify(db['games'])

@app.route('/api/games/<int:game_id>')
def get_game_by_id(game_id):
    response = requests.get(f"{API_URL}/games/{game_id}")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Game niet gevonden"}), 404
    # game = next((g for g in db['games'] if g['id'] == game_id), None)
    # return jsonify(game) if game else ('Game niet gevonden', 404)

if __name__ == '__main__':
    app.run(debug=True)




