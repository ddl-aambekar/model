import os
import requests
import json as js
import time
import logging

logging.basicConfig(level=logging.INFO)
project_name = "model-export-demo"
user_api_key = os.environ['DOMINO_USER_API_KEY']
domino_url = "staging.domino.tech"

def getOwnerId():
	logging.info('Getting ownerId')
	response = requests.get("https://"+domino_url+"/v4/users/self", auth=(user_api_key, user_api_key))
	return response.json()

def getProjectId():
    ownerId = getOwnerId().get("id")
    logging.info('Getting projectId for ownerId: '+ownerId)
    response = requests.get("https://"+domino_url+"/v4/projects?name="+project_name+"&ownerId="+ownerId, auth=(user_api_key, user_api_key))
    return response.json()

def buildModel():
    projectId = getProjectId()[0].get("id")
    logging.info('Building model for projectId: '+projectId)
    headers = {"Content-Type": "application/json", "X-Domino-Api-Key": user_api_key}
    json_data = js.dumps(
    		{
	    		"projectId": ""+projectId+"", 
	    		"inferenceFunctionFile": "model_pip_pkg/model.py",
	    		"inferenceFunctionToCall": "my_model",
	    		"environmentId": None,
	    		"modelName": "My Test Model for via Sublime",
	    		"logHttpRequestResponse": True,
	    		"description": "Testing default model"
    		}
		)
    response = requests.post("https://"+domino_url+"/v4/models/buildModelImage", headers = headers, data = json_data)
    return response.json()

def getModelBuildStatus(buildModelId, buildModelVersionNumber):
	logging.info('Getting build status of model '+buildModelId+' and version number '+buildModelVersionNumber)
	response = requests.get("https://"+domino_url+"/v4/models/"+str(buildModelId)+"/"+str(buildModelVersionNumber)+"/getBuildStatus", auth=(user_api_key, user_api_key))
	return response.json()

def exportModelToExternalRegistry(buildModelId, buildModelVersionNumber):
	logging.info('Exporting model '+buildModelId+' and version number '+buildModelVersionNumber +' to ECR')
	headers = {"Content-Type": "application/json", "X-Domino-Api-Key": user_api_key}
	json_data = js.dumps(
			{
				"registryUrl": "946429944765.dkr.ecr.us-east-1.amazonaws.com",
				"repository": "akshay-test", "tag": "random-number-model",
				"username": "AWS",
				"password": ""+os.environ['ECR_PASSWORD']+""
			}
		)
	response = requests.post("https://"+domino_url+"/v4/models/"+str(buildModelId)+"/"+str(buildModelVersionNumber)+"/exportImageToRegistry", headers = headers, data = json_data)
	return response.json()

if __name__== "__main__":
	buildModelResponse = buildModel()
	buildModelId = buildModelResponse.get("modelId")
	buildModelVersionNumber = buildModelResponse.get("modelVersionId")
	buildModelStatus = getModelBuildStatus(buildModelId, buildModelVersionNumber).get("status")
	logging.info('buildModelStatus is '+buildModelStatus)
	modelBuildIsComplete = False
	numberOfRetries = 0

	while(modelBuildIsComplete is not True):
		logging.info('number of retries: '+str(numberOfRetries)+', build model status: '+str(buildModelStatus))
		buildModelStatus = getModelBuildStatus(buildModelId, buildModelVersionNumber).get("status")
		if(buildModelStatus == "complete"):
			logging.info('Model build is complete. Exporting the model now...')
			exportModelToExternalRegistry(buildModelId, buildModelVersionNumber).get("status")
			modelBuildIsComplete = True
			break
		if(numberOfRetries == 7):
			break
		numberOfRetries += 1
		time.sleep(60) #sleep for 60 seconds


