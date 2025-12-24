package Loki.Alert;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.DumperOptions;

import java.util.Map;
import java.util.List;

@Service
public class LokiService {

    @Value("${LOKI_API_ENDPOINT}")
    private String lokiApiEndpoint;

    @Value("${ORGANIZATION_ID}")
    private String organizationId;
    private final RestTemplate restTemplate = new RestTemplate();
    
    // Configure Yaml to behave similarly to default python dump if needed, 
    // but default should be fine for simple structures.
    private final Yaml yaml;

    public LokiService() {
        DumperOptions options = new DumperOptions();
        options.setDefaultFlowStyle(DumperOptions.FlowStyle.BLOCK);
        this.yaml = new Yaml(options);
    }

    public ResponseEntity<String> createOrUpdateAlertingRuleGroup(String ruleNamespace, String yamlRuleGroupDefinition) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType("application/yaml"));
        headers.add("X-Scope-OrgID",organizationId);

        HttpEntity<String> request = new HttpEntity<>(yamlRuleGroupDefinition, headers);
        String url = lokiApiEndpoint + "/loki/api/v1/rules/" + ruleNamespace;
        
        return restTemplate.postForEntity(url, request, String.class);
    }

    public void deleteAlertingRuleGroup(String ruleNamespace, String ruleName) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("X-Scope-OrgID", organizationId);

        String url = lokiApiEndpoint + "/loki/api/v1/rules/" + ruleNamespace + "/" + ruleName;
        HttpEntity<Void> request = new HttpEntity<>(headers);
        restTemplate.exchange(url, org.springframework.http.HttpMethod.DELETE, request, String.class);
    }

    public Map<String, Object> getAlertingRulesInNamespace(String ruleNamespace) {
        String url = lokiApiEndpoint + "/loki/api/v1/rules/" + ruleNamespace;
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.add("X-Scope-OrgID", organizationId);
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<String> response = restTemplate.exchange(url, org.springframework.http.HttpMethod.GET, entity, String.class);
            Map<String, Object> loaded = yaml.load(response.getBody());
            
            if (loaded != null && loaded.containsKey(ruleNamespace)) {
                 Object namespaceContent = loaded.get(ruleNamespace);
                 if (namespaceContent instanceof List) {
                     List<?> list = (List<?>) namespaceContent;
                     if (!list.isEmpty()) {
                         return (Map<String, Object>) list.get(0);
                     }
                 }
            }
        } catch (Exception e) {
            // Handle 404 or other errors
            return null;
        }
        return null;
    }
    
    public String dumpYaml(Object data) {
        return yaml.dump(data);
    }
    
    public Object loadYaml(String data) {
        return yaml.load(data);
    }
}
