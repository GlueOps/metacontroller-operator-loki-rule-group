import json
import requests
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer


LOKI_GATEWAY_URL = 'http://loki-gateway.glueops-core-loki.svc.cluster.local'
LOKI_GATEWAY_PORT = '80'
LOKI_ENDPOINT = f'{LOKI_GATEWAY_URL}:{LOKI_GATEWAY_PORT}'
LOKI_POST_HEADERS = {"Content-Type": "application/yaml"}


def create_or_update_alerting_rule_group(
    rule_namespace,
    yaml_rule_group_definition
):
    response = requests.post(
        f'{LOKI_ENDPOINT}/loki/api/v1/rules/{rule_namespace}',
        data=yaml_rule_group_definition,
        headers=LOKI_POST_HEADERS
    )  
    return response

def delete_alerting_rule_group(
    rule_namespace,
    rule_name,
):
    response = requests.delete(
        f'{LOKI_ENDPOINT}/loki/api/v1/rules/{rule_namespace}/{rule_name}'
    )
    return response


def get_alerting_rules():
    response = requests.get(
        f'{LOKI_ENDPOINT}/loki/api/v1/rules'
    )
    return yaml.safe_load(response.text)

# Not used, since getting state from the API isn't needed for finalizers
def get_alerting_rules_in_namespace(rule_namespace):
    response = requests.get(
        f'{LOKI_ENDPOINT}/loki/api/v1/rules/{rule_namespace}'
    )
    return yaml.safe_load(response.text)[rule_namespace][0]


class LokiRuleGroupHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length).decode('utf-8')
        request_data = json.loads(request_body)

        parent = request_data['parent']
        rule_group = yaml.dump(parent.get('spec', {}))
        rule_group_namespace = request_data['parent']['spec']['name']
        

        if self.path.endswith('/finalize'):
            # Handle the finalize hook
            response = delete_alerting_rule_group(
                rule_name=rule_group_namespace,
                rule_namespace=rule_group_namespace
            )
            response_data = {
                "finalized": response.ok
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            # Sync the object with the external API
            response = create_or_update_alerting_rule_group(
                rule_namespace=rule_group_namespace,
                yaml_rule_group_definition=rule_group
            )
            if response.ok is True:
                synced = True
            else:
                synced = False

            # Prepare the response for Metacontroller
            response_data = {
                'status': {
                    'synced': synced,
                },
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

HTTPServer(("", 80), LokiRuleGroupHandler).serve_forever()
