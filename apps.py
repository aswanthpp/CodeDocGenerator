import sys

import jsonschema
from flask import *
from flask_cors import CORS
from code_understanding import *
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

qa = None


@app.route('/', methods=['GET'])
def health():
    return "Flask Application is Running", 200


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
    path=payload.get('path',None)
    language=payload.get('language',None)
    global qa
    qa=update_data_store(path,language)
    return jsonify({
                'status': 'Success',
                'response': "Load documents Completed"
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
    response=generate_response(qa,query)
    if(qa is None):
        return jsonify({
            'status': 'Failure',
            'response': 'You need to load the document first, using /load'
        }), 200
    else:
        return jsonify({
                'status': 'Success',
                'response': response
            }), 200

if(__name__=='__main__'):
    if len(sys.argv) != 2:
        print("Usage: python script.py <API_KEY>")
        sys.exit(1)
    else:
        api_key = sys.argv[1]
        os.environ["OPENAI_API_KEY"] = api_key
        print("starting flask app")
        app.run(host='0.0.0.0', port=5050)