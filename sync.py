import json
import logging
import os
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.json_log_formatter import JsonFormatter

from src.lib import(
    create_or_update_alerting_rule_group,
    delete_alerting_rule_group,
)

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
                    LOkI_GATEWAY_URL=LOKI_GATEWAY_URL
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
                    yaml_rule_group_definition=rule_group,
                    LOKI_GATEWAY_URL=LOKI_GATEWAY_URL
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
