<<<<<<< HEAD
# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
=======
# Azure E2E MLops

## Inspirations & references
1. https://github.com/nfmoore/mlops-example-scenarios-test
2. [Azure](https://learn.microsoft.com/en-us/azure/machine-learning/tutorial-pipeline-python-sdk?view=azureml-api-2)

## Overview
AML - Azure Machine Learning
ADO - Azure DevOps

1. ADO-Tasks - Consists of all Azure ML tasks that can be initiated with supplied parameters from ADO variable groups.
2. AzureML/environment - Consists of code to create train and deployment environments in AML.
3. AzureML/src - Consists of AML SDKv2 pipeline to read data, prepare scikit-learn data transformation pipeline, train ML model (Heart disease binary classification model) with hyper parameter tuning, register as an ONNX model.
4. MLOps/AzureML - Consists of all the YAML declarations for online deployment of the registered model and data drift identification.
5. MLOps/ADO - Consists of all the YAML declarations for automating the train pipeline and the deployment pipeline.
6. environment/ - Consists of Terraform IaC for AML creation and deletion.

## Objective

To create an E2E MLOps pipeline to create infrastructure, train a binary classification heart disease model, deploy as an online endpoint and monitor data drifts.

Follow this to setup ADO and AML: https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/machine-learning/how-to-setup-mlops-azureml.md

The story:

1. Create a service connection (ADO x Azure) with Service connection type as "Azure Resource Manager" (ADO -> project settings -> service connections). Use security principal authentication or authentication of your choice.
2. Create a variable group (ADO -> Pipelines -> Library -> Variable Group) and create the key value pairs for the variables (aml_workspace, BASE_NAME, INSTRUMENTATION_KEY, LOCATION, LOG_ANALYTICS_WORKSPACE_ID, resource_group, service_connection_aml, service_connection_rg, train_cluster_name, train_cluster_sku).
3. Execute environment/terraform_iac_create.yml by creating a pipeline run. This step will create the required resources like AML and its associated resources.
4. Create a service connection (ADO x AML).
5. Create a manual trigger pipeline to exeucte /MLOps/ADO/train-pipeline.yml. This will connect to AML workspace, register the base dataset, setup the train environment, create a compute cluster of the specified SKU, runs the training pipeline with hyperparameter tuning (sweeping) and registering the ONNX model.
6. After successfully, executing the previous step execute /MLOps/ADO/deploy-pipeline.yml. This will connect to AML workspace, create environment, create compute cluster, create and deploy the online endpoint.
7. After the above step, we can register a job that runs every 'n' minutes to check the data drift powered by evidently library. The data in the online endpoint is captured by the Azure Log analytics workspace which periodically collects the online data and register as a dataset. The base dataset is now compared it with the new dataset and notifies in case of any any dift in the data.
>>>>>>> d80305f83114bcc3892b7d43966daf50b400210e
