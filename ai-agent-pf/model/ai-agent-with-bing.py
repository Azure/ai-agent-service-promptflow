from promptflow import tool
from azure.ai.projects import AIProjectClient
#from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from promptflow.connections import CustomConnection
import os



@tool
def run_agent_with_bingsearch(input: str, thread_id: str, ai_project_connection: CustomConnection) -> str:
    
    connection_string = ai_project_connection["ConnectionString"]
    agent_id = ai_project_connection["AgentID"]

    project_client = AIProjectClient.from_connection_string(
        credential = ManagedIdentityCredential(client_id=os.getenv("UAI_CLIENT_ID")),
        conn_str=connection_string)

    try:
        agent = project_client.agents.get_agent(agent_id)
    except Exception as e:
        return f"Error: {e}"


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

