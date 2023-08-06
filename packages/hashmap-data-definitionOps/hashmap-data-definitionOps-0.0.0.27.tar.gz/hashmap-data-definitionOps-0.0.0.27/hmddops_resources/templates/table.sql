
-- 
-- DDL_MD5 : {{ ddl.DDL_MD5 }}
-- GEN_DATE : {{ ddl.GENERATE_DATE }}
-- SOURCE : {{ ddl.DB }}.{{ ddl.SCH}}.{{ ddl.OBJ_NAME }}
-- DDL : 
--    {{ ddl.DDL | replace("\n", "\n--") }} 
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

{% if ddl.DETECTION == 'A' %}
  {{ ddl.DDL }}
  

{% elif ddl.DETECTION == 'U' %}

   {% if cols|length >= 1 %}
      -- The following columns have been identified as added/updated
      {% for c in cols %}
          -- {{ c }}
          ALTER TABLE IF EXISTS {{ '"{{ target.DB }}"."{{ target.SCH }}"' }}.{{ ddl.OBJ_NAME }} 
           add column {{ c.OBJ_NAME }} {{ c.DATA_TYPE }} {% if c.COLUMN_DEFAULT is defined %}  DEFAULT {{ c.COLUMN_DEFAULT }} {% endif %}
          ;
      {% endfor %}
    {% endif %}

    -- Also add statements if table level meta information changed like clustering_key
  ;
{% endif %}


