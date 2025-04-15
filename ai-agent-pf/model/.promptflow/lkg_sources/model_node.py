from promptflow import tool
from promptflow.connections import CustomConnection

@tool
def call_ml_model(input: str, model_connection: CustomConnection) -> str:
    import urllib.request
    import json
    import os
    import ssl

    
    data = {
    "topic": "atom"
    }

    body = str.encode(json.dumps(data))

    url = model_connection.url
    # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
    api_key = model_connection.key
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        result_json = json.loads(result)
        output_value = result_json.get("result", "")
        return output_value
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
 