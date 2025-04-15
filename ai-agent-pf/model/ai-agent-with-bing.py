from promptflow import tool
from azure.ai.projects import AIProjectClient
#from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from promptflow.connections import CustomConnection
import os
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

# In Python tool you can do things like calling external services or
# pre/post processing of data, pretty much anything you want


@tool
def run_agent_with_bingsearch(input: str, thread_id: str, ai_project_connection: CustomConnection) -> str:
    
    connection_string = ai_project_connection["ConnectionString"]
    agent_id = ai_project_connection["AgentID"]

    project_client = AIProjectClient.from_connection_string(
        credential = ManagedIdentityCredential(client_id=os.getenv("UAI_CLIENT_ID")),
        #conn_str="westus3.api.azureml.ms;e4718866-4e88-411f-a0b8-10c8051dc165;ai-foundry;anildwa-project-westus3"
        conn_str=connection_string)

    try:
        agent = project_client.agents.get_agent(agent_id)
    except Exception as e:
        return f"Error: {e}"

    #thread = project_client.agents.get_thread("thread_tVlN2nf8ixdbgnRARvLPAnec")
    try:
        thread = project_client.agents.get_thread(thread_id) 
    except Exception as e:
        print(f"Error: {e}")
        thread = project_client.agents.create_thread()
    
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=input
    )

    run = project_client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=agent.id)
    messages = project_client.agents.list_messages(thread_id=thread.id)

    agent_response = {"thread_id": thread.id, "agent_id": agent.id, "message": messages.get_last_text_message_by_role(role="assistant")["text"]["value"]}
    return agent_response["message"]

    #return f"Hello from AI Agent with Bing Search! your input was: {input}"