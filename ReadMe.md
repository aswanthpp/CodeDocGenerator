# Code Doc Generator

Generate response from LLM with a given codbase context. Currently this supports for JAVA and PYTHON

## Build

1. Using Docker
```shell
docker build -t codedoc .
docker run -p 5050:5050 -e OPENAI_API_KEY="<YOUR_OPEN_AI_KEY>" codedoc
```
or 
```shell
docker pull aswanthpp/code_doc_gen_llm:pilot_v.0.0.1
docker run -p 5050:5050 -e OPENAI_API_KEY="<YOUR_OPEN_AI_KEY>" aswanthpp/code_doc_gen_llm:pilot_v.0.0.1
```

2. Using Flask
```shell
pip install -r requirements.txt
export OPENAI_API_KEY="<YOUR_OPEN_AI_KEY>"
python -u app.py                          
```

NB:  Replace <YOUR_OPEN_AI_KEY> with your open api key while running the docker.


## Usage

1. Load codebase to LLM

Create a POST request to the `/load` endpoint, to load custom codebase to LLM<br>
eg: 
```shell
curl --location 'http://localhost:5050/load' \
--header 'Content-Type: application/json' \
--data '{
    "path": "https://github.com/render-examples/flask-hello-world",
    "language": "PYTHON"
}'
```
NB: This is a one time activity for a given codebase, only load if you want load another codebase or change language

2. Generate response from LLM 

Generate LLM response using the information from Custom codebase loaded earlier<br>
eg:
```shell
curl --location 'http://localhost:5050/chat' \
--header 'Content-Type: application/json' \
--data '{
    "query":"which  currency conversions are available?"
}'
```
