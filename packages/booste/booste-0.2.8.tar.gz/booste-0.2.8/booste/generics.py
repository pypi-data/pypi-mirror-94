import numpy as np
import requests
import time
import os
import json
from uuid import uuid4

endpoint = 'https://booste-corporation-v3-flask.zeet.app/'
# Endpoint override for development
if 'BoosteURL' in os.environ:
    print("Dev Mode")
    if os.environ['BoosteURL'] == 'local':
        endpoint = 'http://localhost/'
    else:
        endpoint = os.environ['BoosteURL']
    print("Hitting endpoint:", endpoint)


# identify machine for blind use
cache_path = os.path.abspath(os.path.join(os.path.expanduser('~'),".booste","cache.json"))
if os.path.exists(cache_path):
    with open(cache_path, "r") as file:
        cache = json.load(file)
else:
    cache = {}
    cache['machine_id'] = str(uuid4())
    os.makedirs(os.path.join(os.path.expanduser('~'), ".booste"), exist_ok=True)
    with open(cache_path, "w+") as file:
        json.dump(cache, file)


client_error = {
    "OOB" : "Client error: {}={} is out of bounds.\n\tmin = {}\n\tmax = {}"
}

# THE MAIN FUNCTIONS
# ___________________________________


def run_main(api_key, model_key, model_parameters):
    sync_mode = "synchronous"
    task_id = call_start_api(api_key, model_key, model_parameters, sync_mode)
    # Just hardcode intervals
    interval, initial_wait = 1, 1
    time.sleep(initial_wait)
    while True:
        dict_out = call_check_api(api_key, task_id, sync_mode)
        if dict_out['status'] == "finished":
            return dict_out["output"]
        if dict_out["status"] == "failed":
            raise Exception("Server error: Booste inference job returned status 'failed'")
        time.sleep(interval)
def start_main(api_key, model_key, model_parameters):
    sync_mode = "asynchronous"
    task_id = call_start_api(api_key, model_key, model_parameters, sync_mode)
    return task_id
def check_main(api_key, task_id):
    sync_mode = "asynchronous"
    dict_out = call_check_api(api_key, task_id, sync_mode)
    return dict_out


# THE API CALLING FUNCTIONS
# ________________________

# Takes in start params, returns task ID
def call_start_api(api_key, model_key, model_parameters, sync_mode):
    global endpoint
    route_start = 'inference/start'
    url_start = endpoint + route_start
    global cache
    # sequence = []
    payload = {
        "apiKey" : api_key,
        "modelKey" : model_key,
        "modelParameters" : model_parameters,
        "machineID" : cache['machine_id'],
        "syncMode": sync_mode
    }
    response = requests.post(url_start, json=payload)
    if response.status_code != 200:
        raise Exception("Server error: Booste inference server returned status code {}\n{}".format(
            response.status_code, response.json()['message']))
    try:
        out = response.json()
        task_id = out['taskID']
        return task_id
    except:
        raise Exception("Server error: Failed to return taskID")


# The bare async checker. Used by both gpt2_sync_main (automated) and async (client called)
# Takes in task ID, returns reformatted dict_out with Status and Output
def call_check_api(api_key, task_id, sync_mode):
    global endpoint
    route_check = 'inference/check'
    url_check = endpoint + route_check
    # Poll server for completed task
    payload = {"taskID": task_id, "apiKey": api_key, "syncMode": sync_mode}
    response = requests.post(url_check, json=payload)
    if response.status_code != 200:
        raise Exception("Server error: Booste inference server returned status code {}\n{}".format(
            response.status_code, response.json()['message']))
    out = response.json()
    return out