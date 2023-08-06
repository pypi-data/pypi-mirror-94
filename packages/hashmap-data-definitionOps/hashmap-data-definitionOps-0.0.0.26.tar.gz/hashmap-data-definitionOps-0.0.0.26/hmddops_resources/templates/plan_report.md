
# Phase : PLAN
#### Generated on : {{ report_date }}

#### 

| Type | Name | Detection | Deployment strategy | comment | script_file |
|------|------|-----------|---------------------|---------|-------------|
{% for r in plan %}
{%- set script = r.SCRIPT_FILE.split('/') -%}
|{{ r.OBJ_NAME }} | {{ r.OBJ_NAME }} | {{ r.DETECTION }} | {{ r.DEPLOY_STRATEGY }} | {{ r.DELTA_COMMENT }} | [{{ script[2] }}](../{{ r.SCRIPT_FILE }}) |
{% endfor %}
