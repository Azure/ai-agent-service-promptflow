from promptflow import tool
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from azure.ai.projects.models import MessageRole
from promptflow.connections import CustomConnection
import os



@tool
def run_agent_with_bingsearch(input: str, thread_id: str, connection: CustomConnection) -> str:
    
    connection_string = connection["ConnectionString"]
    agent_id = connection["AgentID"]

    #credential = DefaultAzureCredential() # For local development
    credential = ManagedIdentityCredential(client_id=os.getenv("UAI_CLIENT_ID"))
    project_client = AIProjectClient.from_connection_string(
        credential = credential,
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
    #messages = project_client.agents.list_messages(thread_id=thread.id)
    response_message = project_client.agents.list_messages(thread_id=thread.id).get_last_message_by_role(
        MessageRole.AGENT
    )
    url_citation_annotations = []

    agent_response_message = ""
    for text_message in response_message.text_messages:
        agent_response_message += text_message.text.value + "\n"
    for annotation in response_message.url_citation_annotations:
        uca = {"url_citation.title": annotation.url_citation.title, "url_citation.url": annotation.url_citation.url}
        url_citation_annotations.append(uca)
    


    agent_response = {"thread_id": thread.id, "agent_id": agent.id, "message": agent_response_message, "url_citation_annotations": url_citation_annotations}
    return agent_response

