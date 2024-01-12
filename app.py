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

qa = None

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
    path=payload.get('path',None)
    language=payload.get('language',None)
    # global qa
    # qa=update_data_store(path,language)
    # return jsonify({
    #             'status': 'Success',
    #             'response': "Load documents Completed"
    #         }), 200

    return jsonify({
                'status': 'Success',
                'response': f"Load documents Completed for {path}"
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
    # response=generate_response(qa,query)
    # if(qa is None):
    #     return jsonify({
    #         'status': 'Failure',
    #         'response': 'You need to load the document first, using /load'
    #     }), 200
    # else:
    #     return jsonify({
    #             'status': 'Success',
    #             'response': response
    #         }), 200

    return jsonify({
                'status': 'Success',
                'response': f"Query Fired: {query}"
            }), 200

if(__name__=='__main__'):
    print("Please set env OPENAI_API_KEY, before starting the application")
    print("starting flask app")
    app.run(host='0.0.0.0', port=5050)