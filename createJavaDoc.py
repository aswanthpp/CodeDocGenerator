import sys
import traceback
import openai
import argparse

# Replace with your OpenAI API key
# api_key = "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"
api_key = "temp"

def getOpenAiResponse(prompt):
    try:
        response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose the most appropriate engine
        prompt=prompt,
        max_tokens=150,  # Adjust this based on the desired response length
        api_key=api_key
        )
        return response
    except Exception as err:
        print(traceback.format_exc())
        return "Got Exception from Completion API"

def processInputFile(java_file_path):

    with open(java_file_path, 'r') as file:
        java_code = file.read()

    prompt = f"Generate Javadoc comments for the following Java class and each functions and return the commented java class for the file :\n{java_code}"
    return prompt

    # generated_comments = response.choices[0].text
    # print(generated_comments)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--path', type=str, help="Java File Path", required=True)
        java_file_path = vars(parser.parse_args())['path']
        prompt=processInputFile(java_file_path)
        print(prompt)
        # getOpenAiResponse(prompt)
    except Exception as err:
        print(traceback.format_exc())