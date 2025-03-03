import json
import logging
import os
import yaml
import requests
from pydantic import BaseModel
from fastapi import FastAPI, Request
from typing import Dict, Any
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.json_log_formatter import JsonFormatter


# configure logging
json_formatter = JsonFormatter()

handler = logging.StreamHandler()
handler.setFormatter(json_formatter)

logger = logging.getLogger('LOKI_RULE_GROUP_CONTROLLER')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# configure loki endpoint values
LOKI_API_ENDPOINT = os.environ['LOKI_API_ENDPOINT']
LOKI_POST_HEADERS = {"Content-Type": "application/yaml"}

app = FastAPI()

class StringPayload(BaseModel):
    text: str

def create_or_update_alerting_rule_group(
    rule_namespace,
    yaml_rule_group_definition,
):
    response = requests.post(
        f'{LOKI_API_ENDPOINT}/loki/api/v1/rules/{rule_namespace}',
        data=yaml_rule_group_definition,
        headers=LOKI_POST_HEADERS
    )  
    return response

def delete_alerting_rule_group(
    rule_namespace,
    rule_name,
):
    response = requests.delete(
        f'{LOKI_API_ENDPOINT}/loki/api/v1/rules/{rule_namespace}/{rule_name}'
    )
    return response

def get_alerting_rules():
    response = requests.get(
        f'{LOKI_API_ENDPOINT}/loki/api/v1/rules'
    )
    return yaml.safe_load(response.text)

# Not used, since getting state from the API isn't needed for finalizers
def get_alerting_rules_in_namespace(rule_namespace,):
    response = requests.get(
        f'{LOKI_API_ENDPOINT}/loki/api/v1/rules/{rule_namespace}'
    )
    return yaml.safe_load(response.text)[rule_namespace][0]


@app.get("/sync")
def post(request_body: Dict[str, Any]):
    request_data = json.loads(request_body)
    parent = request_data['parent']
    rule_group = yaml.dump(parent.get('spec', {}))
    try:
            rule_group_namespace = request_data['parent']['spec']['name']
    except Exception:
            status = 'Degraded'
            logger.exception(f'failed to parse request: {request_data}')
    try:        
        response = create_or_update_alerting_rule_group(
                    rule_namespace=rule_group_namespace,
                    yaml_rule_group_definition=rule_group
                )
                # check if rule group was created
        if yaml.safe_load(rule_group) == get_alerting_rules_in_namespace(
                    rule_namespace=rule_group_namespace
        ):
                    status = 'Healthy'
        else:
                    status = 'Progressing'
    except Exception:
                status = "Degraded"
                logger.exception(f'failed to create rule group: {rule_group}')
    response_data = {
                'status': {
                    'health': {
                        'status': status 
                    },
                },
            }                      

    return response_data

@app.post("/finalize")
def finalize(request_body: Dict[str, Any]):
    request_data = json.loads(request_body)
    parent = request_data['parent']
    rule_group = yaml.dump(parent.get('spec', {}))
    try:
            rule_group_namespace = request_data['parent']['spec']['name']
    except Exception:
            status = 'Degraded'
            logger.exception(f'failed to parse request: {request_data}')
    try:
                response = delete_alerting_rule_group(
                    rule_name=rule_group_namespace,
                    rule_namespace=rule_group_namespace,
                )
                response_data = {
                    "finalized": response.ok
                }
                return {response_data}
    except Exception:
                response_data = {
                    "finalized": True
                }
                return {response_data}    
    

