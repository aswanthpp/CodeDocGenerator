import sys

import jsonschema
from flask import *
from static.lib.utils import *
app = Flask(__name__)
load_data_schema = {
"type": "object",
"properties": {
    "path": {"type": "string"},
    "language": {"type": "string"}
    },
"required": ["path","language"]
}


query_data_schema = {
"type": "object",
"properties": {
    "query": {"type": "string"}
    },
"required": ["query"]
}

flask_app_loader = LangChainCodeLoder(qa = None)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load', methods=['POST'])
def load_documents_to_store():
    try:
        payload = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'status': 'Failure',
            'message': 'The request body is not a valid JSON.'
        }), 400
    try:
        jsonschema.validate(instance=payload, schema=load_data_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({
            'status': 'Failure',
            'message': "Schema Varildation Failed, Mandatory Fields are missing.`path` and `language` are mandatory key in payload"

        }), 200
    try:
        path=payload.get('path',None)
        language=payload.get('language',None)
        response_json=flask_app_loader.update_data_store(path,language)
        return jsonify(response_json), 200
    except Exception as e:
        print(f"Got exception in loading codebase: {e}")
        return jsonify({
            'status': 'Failure',
            'message': "Please set Valid OPEN_API_KEY as Env, or Enter public Github url"

        }), 200


@app.route('/chat', methods=['POST'])
def get_response():
    try:
        payload = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'status': 'Failure',
            'message': 'The request body is not a valid JSON.'
        }), 400
    try:
        jsonschema.validate(instance=payload, schema=query_data_schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({
            'status': 'Failure',
            'message': "Schema Varildation Failed, Mandatory Fields are missing.`query` is mandatory key in payload"

        }), 200
    query=payload.get('query',None)
    response=flask_app_loader.generate_response(query)
    if(response is None):
        return jsonify({
            'status': 'Failure',
            'message': 'You need to load the document first, using /load'
        }), 200
    else:
        return jsonify({
                'status': 'Success',
                'message': response
            }), 200

if(__name__=='__main__'):
    print("Please set env OPENAI_API_KEY, before starting the application")
    print("starting flask app")
    app.run(host='0.0.0.0', port=5050)