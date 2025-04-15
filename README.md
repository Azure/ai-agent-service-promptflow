# 🚀 Grounding with Bing Search using Azure AI Agent & Promptflow


This repository demonstrates how to implement and deploy an AI Agent grounded with Bing Search using Azure AI Agent service and Promptflow. The entire solution is hosted as an Azure AI Foundry deployment endpoint.

Azure AI Agent requires an Agent ID and a thread id. The thread id is an optional parameter that can be used to track the conversation context. The Agent ID is configured in the custom connection resource and is not required as input parameter.

If the thread id is not provided, the agent will create a new thread for each conversation. The agent will use the thread id to keep track of the conversation context and will use it to generate responses. The agent will use bing search to find relevant information and will use it to generate responses. 

Key components:
- **Promptflow** orchestrates the AI Agent logic.
- **Azure AI Agent service** powers the LLM agent.
- **Azure AI Foundry** hosts the deployment and manages the lifecycle.
- **Custom connection resources** and agent setup streamline secure configuration.

---

## ✅ Prerequisites

Make sure you have the following tools and resources set up:

### Azure Resources
- ✅ Azure AI Foundry project
- ✅ *Grounding with Bing Search* resource added to your AI Project

### Tools
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed and authenticated
- Azure ML extension for Azure CLI:
  ```bash
  az extension add -n ml
  ```

- Azure AI Foundry CLI installed and configured (based on project docs)

---

## 🧠 Step 1: Create Agent in Azure AI Project

1. **Create an Agent** in the AI Project and add the tool:  
   **`Grounding with Bing Search`**

2. **Configure Agent Instructions**:

   ```
   You are a helpful assistant. You can answer end user questions. 
   You have access to Bing Search. Use Bing Search only when needed.
   ```

3. **Note the Agent ID** – you'll need it in later steps.

---

## 🔐 Step 2: Create Custom Connection

Create a **Custom Connection** in the AI Project connected resources panel.
You might need to create a dummy secret to save the connection.

| Key               | Value                                                                 |
|------------------|-----------------------------------------------------------------------|
| `ConnectionString` | `westus3.api.azureml.ms;<GUID>;ai-foundry;<AI Project Name>` |
| `AgentID`        | `"asst_UlhICUu5wEq4DqWc2HpUZawN"`                                     |

---

## 🌐 Step 3: Create AML Online Endpoint

1. Navigate to the deployment folder:
   ```bash
   cd aml-endpoint-deployment
   az configure --defaults workspace=<AI Project Name> group=<ai-project resource group>
   ```

2. Create the Azure ML online endpoint:
   ```bash
   az ml online-endpoint create -f pf_endpoint.yml
   ```

3. Grant the **Managed Identity** of the endpoint the `Azure AI Administrator` role in the AI Project.

---

## 🧪 Step 4: Build Custom Environment

1. Navigate to the image build folder:
   ```bash
   cd pf_image_build
   ```

2. Create the environment:
   ```bash
   az ml environment create -f environment.yml
   ```

3. Wait for the build to complete. Once built, **note the Azure container registry path**.

---

## 📦 Step 5: Upload Promptflow Model

1. Update the `version` in `pf_model.yml` to reflect a new version for each deployment.
2. From the deployment folder:
   ```bash
   cd ../aml-endpoint-deployment
   az ml model create -f pf_model.yml
   ```

---

## 🛠 Step 6: Update Deployment Configuration

Edit `pf_deployment.yml` and:
- Update the image name using the values from Step 4.
- Update the model version to match Step 5.


---

## 🚀 Step 7: Deploy to AML Online Endpoint

```bash
az ml online-deployment create --name blue --endpoint-name <your-endpoint-name> -f pf_deployment.yml
```

Replace `<your-endpoint-name>` with the endpoint name used in `pf_endpoint.yml`.

---

## 💡 Example Deployment Folder Structure

```
.
AI-AGENT-PROMPTFLOW
├── ai-agent-pf-docker
│   ├── model
│   ├── __pycache__
│   ├── .promptflow
│   ├── ai-agent-with-bing.py
│   ├── flow.dag.yaml
│   ├── flow.meta.yaml
│   ├── requirements.txt
│   └── samples.json
│
├── aml-endpoint-deployment
│   ├── aml_env.yml
│   ├── pf_deployment.yml
│   ├── pf_deployment_concurrent_requests.yml
│   ├── pf_endpoint.yml
│   └── pf_model.yml
│
├── pf_image_build
│   ├── Dockerfile
│   ├── environment.yml
│   └── requirements.txt
│
├── sample_pf_input.json
├── aml-endpoint-test.py
└── README.md

```
---

## 📤 Sample Payload

```json
{
    "topic": "what is the capital of France?",
    "thread_id": "test_thread1"
}
```

## 🧼 Cleanup Resources (Optional)

To delete the online endpoint:

```bash
az ml online-endpoint delete --name <your-endpoint-name>
```

---

## 📝 Notes

- All connected resources, including the Agent, must be correctly referenced in the AI Project for the deployment to succeed.
- Use Azure ML Studio or the CLI to monitor logs and deployment status.
- Always increment model and environment versions when making changes.



## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.