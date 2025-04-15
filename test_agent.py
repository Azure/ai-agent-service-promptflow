# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use agent operations with the Bing grounding tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python sample_agents_bing_grounding.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
    3) BING_CONNECTION_NAME - The connection name of the Bing connection, as found in the 
       "Connected resources" tab in your Azure AI Foundry project.
"""

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole, BingGroundingTool
from azure.identity import DefaultAzureCredential


project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="westus3.api.azureml.ms;e4718866-4e88-411f-a0b8-10c8051dc165;ai-foundry;anildwa-project-westus3",
)

# [START create_agent_with_bing_grounding_tool]
bing_connection = project_client.connections.get(connection_name="anildwabinggrounding")
conn_id = bing_connection.id

print(conn_id)

# Initialize agent bing tool and add the connection id
bing = BingGroundingTool(connection_id=conn_id)

# Create agent with the bing tool and process assistant run
with project_client:
    agent = project_client.agents.get_agent("asst_wuuERC4L0LKfqUGZR2jEO2nW")
    thread = project_client.agents.get_thread("thread_IQ0YuqHlij9gIYBA5Hvnf2s5") 
    # Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="How does wikipedia explain Euler's Identity?",
    )
    print(f"Created message, ID: {message.id}")

    # Create and process agent run in thread with tools
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the assistant when done
    #project_client.agents.delete_agent(agent.id)
    #print("Deleted agent")

    # Print the Agent's response message with optional citation
    response_message = project_client.agents.list_messages(thread_id=thread.id).get_last_message_by_role(
        MessageRole.AGENT
    )
    if response_message:
        for text_message in response_message.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in response_message.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")