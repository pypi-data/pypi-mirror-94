

-- 
-- GEN_DATE : {{ GENERATE_DATE }}
-- SOURCE : {{ DB }}.{{ SCH }}
-- 

--REM
--REM DELETE THE BELOW HELPER SECTION
--REM   These sections will be removed during planning phase
--REM 
--REM   {{ ddl | replace("\n", "\n--REM ") }} 
--REM 
--REM  
--REM Environment variables has been configured under os_env
--REM 

--REM TODO GRANT OWNERSHIP ON FUNCTION DEV_RAW.TPCDS_SF10TCL.WEATHERCATEGORICAL(DT VARCHAR) TO ROLE DEV_DBA;
--REM 

{% for g in grants %}
  -- originally given to role {{ g['GRANTEE'] }}
  GRANT {{ g['PRIVILEGE_TYPE'] }} ON {{ g['GRANT_OBJECT_TYPE'] }} {{ '"{{ target.DB }}"."{{ target.SCH }}".' }}{{ g['MOD_OBJ_NAME'] }} TO ROLE {{ '{{ keyword_map.DBA }}' }} ;

{% endfor %}

