from flask import Flask, request, send_from_directory
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'dict_manager.html')

@app.route('/base_english_grammar.txt')
def get_base_dictionary():
    return send_from_directory('.', 'base_english_grammar.txt')

@app.route('/dynamic_dictionary.json')
def get_dynamic_dictionary():
    return send_from_directory('.', 'dynamic_dict.json')

@app.route('/save_base_dictionary', methods=['POST'])
def save_base_dictionary():
    data = request.data.decode('utf-8')
    with open('base_english_grammar.txt', 'w', encoding='utf-8') as file:
        file.write(data)
    return '', 204

@app.route('/save_dynamic_dictionary', methods=['POST'])
def save_dynamic_dictionary():
    data = request.data.decode('utf-8')
    with open('dynamic_dict.json', 'w', encoding='utf-8') as file:
        file.write(data)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
