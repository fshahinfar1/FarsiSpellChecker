import json
from flask import Flask, request, jsonify, make_response
from src.farsi_spell_checker import FSpellChecker

app = Flask(__name__)
spell_checker = FSpellChecker(2)


@app.route('/')
def index():
    return "Farsi spell checker is online"


@app.route('/spell_check', methods=['POST',])
def spell_check():
    print(request.data)
    txt = json.loads(request.data).get('txt')
    if txt is None:
        abort(400)
    mistakes = spell_checker.spell_check(txt)
    result = dict()
    for mist in mistakes:
        token = mist.token
        result[token] = mist.suggestions 
    return jsonify(result)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port)

