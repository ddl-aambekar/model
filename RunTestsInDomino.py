import os
import requests
import json as js
import time
import logging

logging.basicConfig(level=logging.INFO)
user_api_key = os.environ['DOMINO_USER_API_KEY']
with open('setup.py') as f:
    c = f.read()
    
TAG = c.partition('version=')[2].partition(',')[0]

def getOwnerId():
	logging.info('Getting ownerId')
	response = requests.get("https://"+domino_url+"/v4/users/self", auth=(user_api_key, user_api_key))
	return response.json()

def getProjectId():
    ownerId = getOwnerId().get("id")
    logging.info('Getting projectId for ownerId: '+ownerId)
    response = requests.get("https://"+domino_url+"/v4/projects?name="+project_name+"&ownerId="+ownerId, auth=(user_api_key, user_api_key))
    return response.json()

def startJobTests():
    projectId = getProjectId()[0].get("id")
    logging.info('Starting tests for projectId: '+projectId)
    headers = {"Content-Type": "application/json", "X-Domino-Api-Key": user_api_key}
    https://demo.dominodatalab.com/v1/projects/amj2403/model-ops-demo/runs
    json_data = js.dumps(
    		{
	    		"command": [
	    		  "run_tests.py"
	    		],
	    		"inferenceFunctionFile": "model_pip_pkg/model.py",
	    		"inferenceFunctionToCall": "my_model",
	    		"environmentId": None,
	    		"modelName": "My Test Model built in workshop",
	    		"logHttpRequestResponse": True,
	    		"description": "Testing default model"
    		}
		)
    response = requests.post("https://"+domino_url+"/v1/projects/amj2403/"+project_name+"/runs", headers = headers, data = json_data)
    return response.json()


if __name__== "__main__":

	project_name = "model-ops-demo"
	domino_url = "demo.dominodatalab.com"

	logging.info("Starting tests")