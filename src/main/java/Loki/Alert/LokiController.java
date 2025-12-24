package Loki.Alert;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.HashMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class LokiController {

    private static final Logger logger = LoggerFactory.getLogger(LokiController.class);

    @Autowired
    private LokiService lokiService;

    @PostMapping("/sync")
    public Map<String, Object> sync(@RequestBody Map<String, Object> requestData) {
        String status = "Degraded";
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> parent = (Map<String, Object>) requestData.get("parent");
            @SuppressWarnings("unchecked")
            Map<String, Object> spec = (Map<String, Object>) parent.get("spec");
            String ruleGroupNamespace = (String) spec.get("name");
            
            String ruleGroupYaml = lokiService.dumpYaml(spec);
            
            try {
                lokiService.createOrUpdateAlertingRuleGroup(ruleGroupNamespace, ruleGroupYaml);
                
                // Verification
                Object loadedYaml = lokiService.loadYaml(ruleGroupYaml);
                Map<String, Object> remoteRules = lokiService.getAlertingRulesInNamespace(ruleGroupNamespace);
                
                if (loadedYaml.equals(remoteRules)) {
                    status = "Healthy";
                } else {
                    status = "Progressing";
                }
                
            } catch (Exception e) {
                status = "Degraded";
                logger.error("Failed to create rule group: " + ruleGroupYaml, e);
            }
            
        } catch (Exception e) {
            status = "Degraded";
            logger.error("Failed to parse request: " + requestData, e);
        }

        Map<String, Object> response = new HashMap<>();
        Map<String, Object> statusMap = new HashMap<>();
        Map<String, Object> healthMap = new HashMap<>();
        healthMap.put("status", status);
        statusMap.put("health", healthMap);
        response.put("status", statusMap);
        
        return response;
    }

    @PostMapping("/finalize")
    public Map<String, Object> finalize(@RequestBody Map<String, Object> requestData) {
        boolean finalized = true;
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> parent = (Map<String, Object>) requestData.get("parent");
            @SuppressWarnings("unchecked")
            Map<String, Object> spec = (Map<String, Object>) parent.get("spec");
            String ruleGroupNamespace = (String) spec.get("name");
            
            try {
                lokiService.deleteAlertingRuleGroup(ruleGroupNamespace, ruleGroupNamespace);
                finalized = true;
            } catch (Exception e) {
                finalized = true;
            }
        } catch (Exception e) {
            logger.error("Failed to parse request: " + requestData, e);
            finalized = true;
        }
        
        Map<String, Object> response = new HashMap<>();
        response.put("finalized", finalized);
        return response;
    }
}
