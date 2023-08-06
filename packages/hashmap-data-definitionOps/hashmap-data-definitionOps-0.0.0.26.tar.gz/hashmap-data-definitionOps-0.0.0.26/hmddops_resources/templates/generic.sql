

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

{{ ddl.DDL }}
;


