import requests
import yaml


def create_or_update_alerting_rule_group(
    rule_namespace,
    yaml_rule_group_definition,
    LOKI_GATEWAY_URL,
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
    LOkI_GATEWAY_URL,
):
    response = requests.delete(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules/{rule_namespace}/{rule_name}'
    )
    return response

def get_alerting_rules(LOKI_GATEWAY_URL):
    response = requests.get(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules'
    )
    return yaml.safe_load(response.text)

# Not used, since getting state from the API isn't needed for finalizers
def get_alerting_rules_in_namespace(
    rule_namespace,
    LOkI_GATEWAY_URL,
):
    response = requests.get(
        f'{LOKI_GATEWAY_URL}/loki/api/v1/rules/{rule_namespace}'
    )
    return yaml.safe_load(response.text)[rule_namespace][0]