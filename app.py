from flask import Flask, render_template, request
import flask
import requests
import os
import uuid
import json
from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def index_post():
    original_text = request.form['text']
    target_language = request.form['language']

    print(os.environ)
    
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    path = '/translate?api-version=3.0'
    param_lang = f'&to={target_language}'

    url = endpoint + path + param_lang

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]

    translator_request = requests.post(url, headers=headers, json=body)
    response = translator_request.json()
    translated = response[0]['translations'][0]['text']

    return render_template('results.html', translated_text=translated, original_text=original_text, target_language=target_language
                           )

if __name__ == '__main__':
    app.run()