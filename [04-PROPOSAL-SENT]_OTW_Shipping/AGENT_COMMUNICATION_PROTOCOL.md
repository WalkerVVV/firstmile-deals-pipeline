# AGENT COMMUNICATION PROTOCOL: Shipping Analysis System

## Overview
This document defines the standardized communication protocol for the multi-agent shipping analysis system, ensuring efficient parallel processing and data consistency.

## 1. MESSAGE STRUCTURE

### Standard Message Format
```json
{
    "header": {
        "message_id": "UUID",
        "timestamp": "2024-11-15T10:30:00Z",
        "sender": "agent_id",
        "recipient": "agent_id | orchestrator | broadcast",
        "message_type": "request | response | status | error",
        "priority": "critical | high | normal | low",
        "correlation_id": "UUID"
    },
    "body": {
        "action": "string",
        "data": {},
        "metadata": {}
    },
    "routing": {
        "reply_to": "agent_id",
        "timeout": 60,
        "retry_count": 0
    }
}
```

## 2. MESSAGE TYPES

### 2.1 Task Assignment (Orchestrator → Sub-Agent)
```json
{
    "header": {
        "message_type": "request",
        "sender": "orchestrator",
        "recipient": "data_processing_agent"
    },
    "body": {
        "action": "process_shipping_data",
        "data": {
            "file_path": "shipping_data.csv",
            "validation_rules": {
                "required_columns": ["tracking", "weight", "zone"],
                "weight_range": [0.01, 150],
                "zone_range": [1, 8]
            }
        },
        "metadata": {
            "expected_rows": 10000,
            "deadline": "2024-11-15T10:31:00Z"
        }
    }
}
```

### 2.2 Status Update (Sub-Agent → Orchestrator)
```json
{
    "header": {
        "message_type": "status",
        "sender": "rate_calculator_agent",
        "recipient": "orchestrator"
    },
    "body": {
        "action": "progress_update",
        "data": {
            "task": "calculate_rates",
            "progress_percentage": 65,
            "rows_processed": 6500,
            "estimated_completion": "2024-11-15T10:30:45Z"
        }
    }
}
```

### 2.3 Data Request (Sub-Agent → Sub-Agent)
```json
{
    "header": {
        "message_type": "request",
        "sender": "savings_calculator_agent",
        "recipient": "rate_calculator_agent"
    },
    "body": {
        "action": "get_rate_data",
        "data": {
            "tracking_numbers": ["1Z123", "1Z124"],
            "fields_needed": ["current_cost", "xparcel_cost"]
        }
    }
}
```

### 2.4 Result Response (Sub-Agent → Orchestrator)
```json
{
    "header": {
        "message_type": "response",
        "sender": "zone_analyst_agent",
        "recipient": "orchestrator",
        "correlation_id": "original_request_id"
    },
    "body": {
        "action": "analysis_complete",
        "data": {
            "zone_distribution": {...},
            "zone_savings": {...},
            "optimization_opportunities": [...]
        },
        "metadata": {
            "processing_time": 42.3,
            "rows_analyzed": 10000,
            "warnings": []
        }
    }
}
```

### 2.5 Error Notification
```json
{
    "header": {
        "message_type": "error",
        "sender": "weight_analyst_agent",
        "recipient": "orchestrator",
        "priority": "high"
    },
    "body": {
        "action": "error_report",
        "data": {
            "error_code": "INVALID_WEIGHT_DATA",
            "error_message": "Found 150 packages with weight > 150 lbs",
            "affected_rows": [101, 102, 103],
            "suggested_action": "validate_or_exclude"
        }
    }
}
```

## 3. DATA SHARING PROTOCOL

### 3.1 Shared Data Store Structure
```yaml
shared_data_store:
    cleaned_data:
        owner: data_processing_agent
        access: read_all
        format: dataframe
        last_updated: timestamp

    rate_calculations:
        owner: rate_calculator_agent
        access: read_all
        format: array
        last_updated: timestamp

    zone_analysis:
        owner: zone_analyst_agent
        access: read_all
        format: dictionary
        last_updated: timestamp

    weight_analysis:
        owner: weight_analyst_agent
        access: read_all
        format: dictionary
        last_updated: timestamp

    service_mappings:
        owner: service_mapper_agent
        access: read_all
        format: dictionary
        last_updated: timestamp

    savings_metrics:
        owner: savings_calculator_agent
        access: read_all
        format: dictionary
        last_updated: timestamp
```

### 3.2 Data Access Pattern
```python
# Write Pattern (Producer)
def publish_data(agent_id, data_key, data):
    message = {
        "header": {
            "message_type": "data_publish",
            "sender": agent_id
        },
        "body": {
            "action": "publish_data",
            "data": {
                "key": data_key,
                "value": data,
                "schema_version": "1.0"
            }
        }
    }
    send_to_orchestrator(message)

# Read Pattern (Consumer)
def request_data(agent_id, data_key):
    message = {
        "header": {
            "message_type": "data_request",
            "sender": agent_id
        },
        "body": {
            "action": "request_data",
            "data": {
                "key": data_key,
                "fields": "all"
            }
        }
    }
    return send_and_wait(message)
```

## 4. SYNCHRONIZATION MECHANISMS

### 4.1 Phase Gates
```yaml
phase_1_complete:
    required_agents: [data_processing_agent]
    validation: cleaned_data_exists
    next_phase: phase_2

phase_2_complete:
    required_agents:
        - rate_calculator_agent
        - zone_analyst_agent
        - weight_analyst_agent
        - service_mapper_agent
    validation: all_analysis_complete
    next_phase: phase_3

phase_3_complete:
    required_agents: [savings_calculator_agent]
    validation: savings_metrics_exists
    next_phase: phase_4

phase_4_complete:
    required_agents: [report_builder_agent]
    validation: excel_workbook_created
    next_phase: complete
```

### 4.2 Dependency Management
```json
{
    "agent_dependencies": {
        "data_processing_agent": [],
        "rate_calculator_agent": ["data_processing_agent"],
        "zone_analyst_agent": ["data_processing_agent"],
        "weight_analyst_agent": ["data_processing_agent"],
        "service_mapper_agent": ["data_processing_agent"],
        "savings_calculator_agent": [
            "rate_calculator_agent",
            "zone_analyst_agent",
            "weight_analyst_agent",
            "service_mapper_agent"
        ],
        "report_builder_agent": ["savings_calculator_agent"]
    }
}
```

## 5. BROADCAST MESSAGES

### 5.1 Phase Transition Broadcast
```json
{
    "header": {
        "message_type": "broadcast",
        "sender": "orchestrator",
        "recipient": "all_agents"
    },
    "body": {
        "action": "phase_transition",
        "data": {
            "completed_phase": "phase_1",
            "starting_phase": "phase_2",
            "agents_to_activate": [
                "rate_calculator_agent",
                "zone_analyst_agent",
                "weight_analyst_agent",
                "service_mapper_agent"
            ]
        }
    }
}
```

### 5.2 Emergency Stop
```json
{
    "header": {
        "message_type": "broadcast",
        "sender": "orchestrator",
        "recipient": "all_agents",
        "priority": "critical"
    },
    "body": {
        "action": "emergency_stop",
        "data": {
            "reason": "critical_error",
            "save_state": true
        }
    }
}
```

## 6. PERFORMANCE MONITORING

### 6.1 Heartbeat Message
```json
{
    "header": {
        "message_type": "heartbeat",
        "sender": "agent_id"
    },
    "body": {
        "data": {
            "status": "active",
            "cpu_usage": 45.2,
            "memory_usage": 312.5,
            "queue_depth": 5,
            "current_task": "processing_zones"
        }
    }
}
```

### 6.2 Performance Metrics
```json
{
    "header": {
        "message_type": "metrics",
        "sender": "agent_id"
    },
    "body": {
        "data": {
            "tasks_completed": 10,
            "average_processing_time": 4.5,
            "success_rate": 100,
            "error_count": 0
        }
    }
}
```

## 7. ERROR HANDLING & RECOVERY

### 7.1 Retry Protocol
```yaml
retry_policy:
    max_attempts: 3
    backoff_strategy: exponential
    initial_delay: 1s
    max_delay: 30s
    retry_on_errors:
        - TIMEOUT
        - TEMPORARY_FAILURE
        - RESOURCE_UNAVAILABLE
```

### 7.2 Failure Cascade Prevention
```python
def handle_agent_failure(failed_agent, error):
    # 1. Isolate failed agent
    quarantine_agent(failed_agent)

    # 2. Notify dependent agents
    for dependent in get_dependents(failed_agent):
        send_warning(dependent, "upstream_failure")

    # 3. Attempt recovery
    if can_recover(error):
        restart_agent(failed_agent)
    else:
        activate_fallback_agent(failed_agent)

    # 4. Reprocess affected data
    reprocess_from_checkpoint(failed_agent.last_checkpoint)
```

## 8. DATA CONSISTENCY GUARANTEES

### 8.1 Version Control
```json
{
    "data_version": {
        "cleaned_data": "v1.2.3",
        "rate_calculations": "v1.0.1",
        "schema_version": "2024.11.15"
    }
}
```

### 8.2 Conflict Resolution
```yaml
conflict_resolution:
    strategy: last_write_wins
    validation: checksum_verification
    audit_trail: enabled
    rollback: supported
```

## 9. SECURITY & AUTHENTICATION

### 9.1 Agent Authentication
```json
{
    "header": {
        "auth_token": "JWT_TOKEN",
        "agent_signature": "SHA256_HASH"
    }
}
```

### 9.2 Data Encryption
- All inter-agent messages encrypted with TLS 1.3
- Sensitive data fields marked for additional encryption
- PII data handling compliant with privacy regulations

## 10. MONITORING & LOGGING

### 10.1 Log Format
```json
{
    "timestamp": "2024-11-15T10:30:00Z",
    "level": "INFO",
    "agent": "agent_id",
    "message": "Processing complete",
    "context": {
        "task_id": "UUID",
        "duration": 42.3,
        "records_processed": 10000
    }
}
```

### 10.2 Audit Trail
```yaml
audit_events:
    - task_assigned
    - data_published
    - data_accessed
    - error_occurred
    - task_completed
    - phase_transitioned
```

## 11. PERFORMANCE OPTIMIZATION

### 11.1 Batch Processing
```json
{
    "batch_config": {
        "batch_size": 1000,
        "parallel_batches": 4,
        "batch_timeout": 30
    }
}
```

### 11.2 Caching Strategy
```yaml
cache_policy:
    rate_calculations:
        ttl: 3600
        strategy: LRU
    zone_mappings:
        ttl: 86400
        strategy: static
    service_mappings:
        ttl: 86400
        strategy: static
```

## 12. SCALABILITY PROVISIONS

### 12.1 Agent Scaling
```yaml
scaling_rules:
    rate_calculator_agent:
        min_instances: 1
        max_instances: 5
        scale_up_threshold: 80% CPU
        scale_down_threshold: 20% CPU

    report_builder_agent:
        min_instances: 1
        max_instances: 3
        scale_up_threshold: queue_depth > 10
```

### 12.2 Load Balancing
```json
{
    "load_balancing": {
        "strategy": "round_robin",
        "health_check_interval": 10,
        "failover_enabled": true
    }
}
```

## Implementation Notes

1. **Message Queue**: Use RabbitMQ or Redis for message passing
2. **Data Store**: Use Redis for shared data with TTL
3. **Monitoring**: Integrate with Prometheus/Grafana
4. **Logging**: Centralized logging with ELK stack
5. **Orchestration**: Consider Apache Airflow or Prefect for workflow management

This protocol ensures efficient parallel processing while maintaining data consistency and system reliability.