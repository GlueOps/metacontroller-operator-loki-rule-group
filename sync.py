import json
import logging
import os
import yaml
import requests

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
LOKI_GATEWAY_URL = os.environ['LOKI_GATEWAY_URL']
LOKI_POST_HEADERS = {"Content-Type": "application/yaml"}

def create_or_update_alerting_rule_group(
    rule_namespace,
    yaml_rule_group_definition,
):
    response = requests.post(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules/{rule_namespace}',
        data=yaml_rule_group_definition,
        headers=LOKI_POST_HEADERS
    )  
    return response

def delete_alerting_rule_group(
    rule_namespace,
    rule_name,
):
    response = requests.delete(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules/{rule_namespace}/{rule_name}'
    )
    return response

def get_alerting_rules():
    response = requests.get(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules'
    )
    return yaml.safe_load(response.text)

# Not used, since getting state from the API isn't needed for finalizers
def get_alerting_rules_in_namespace(rule_namespace,):
    response = requests.get(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules/{rule_namespace}'
    )
    return yaml.safe_load(response.text)[rule_namespace][0]



class LokiRuleGroupHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length).decode('utf-8')
        request_data = json.loads(request_body)

        parent = request_data['parent']
        rule_group = yaml.dump(parent.get('spec', {}))
        try:
            rule_group_namespace = request_data['parent']['spec']['name']
        except Exception:
            status = 'Degraded'
            logger.exception(f'failed to parse request: {request_data}')

        if self.path.endswith('/finalize'):
            # Handle the finalize hook
            try:
                response = delete_alerting_rule_group(
                    rule_name=rule_group_namespace,
                    rule_namespace=rule_group_namespace,
                )
                response_data = {
                    "finalized": response.ok
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception:
                response_data = {
                    "finalized": False
                }
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                logger.exception(f'failed to delete rule group: {rule_group_namespace}/{rule_group_namespace}')

        else:
            # Sync the object with the external API
            try:
                response = create_or_update_alerting_rule_group(
                    rule_namespace=rule_group_namespace,
                    yaml_rule_group_definition=rule_group
                )
                if response.ok is True:
                    status = 'Healthy'
                else:
                    status = 'Progressing'
            except Exception:
                status = "Degraded"
                logger.exception(f'failed to create rule group: {rule_group}')


            # Prepare the response for Metacontroller
            response_data = {
                'status': {
                    'health': {
                        'status': status 
                    },
                },
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

HTTPServer(("", 80), LokiRuleGroupHandler).serve_forever()
