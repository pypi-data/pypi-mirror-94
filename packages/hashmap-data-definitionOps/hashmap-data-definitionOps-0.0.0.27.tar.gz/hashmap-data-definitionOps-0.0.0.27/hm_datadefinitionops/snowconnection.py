"""
    Holds functionalities that interacts with Snowflake
"""
import os
import json
import logging
import confuse
import csv
import re
import pandas as pd
from snowflake import connector
from snowflake.connector.converter_null import SnowflakeNoConverterToPython
from snowflake.connector import DictCursor
from snowflake.connector.constants import QueryStatus

"""
    Base class that is used for connecting and disconnecting 
    with Snowflake
"""


class SnowflakeConnection:
    # True once Snowflake configured and connection established
    initialized = False

    # Snowflake connection object
    sqlconn = None

    # TODO can we make this configurable ?
    logging.getLogger("snowflake.connector").setLevel(logging.WARNING)

    """ 
        class constructor
        - p_db : Database to connect
        - p_schema : Specific schema in the specified database
    """

    def __init__(self, p_db, p_schema):
        self.logger = logging.getLogger(__name__)
        self.db = p_db
        self.schema = p_schema

    """
        Opens connection with Snowflake.
        - p_query_tag : sets the query session tag, which is helpful to identify interactions initied by the tool.

        The information used for connecting to Snowflake is based of using
        snowsql environment variables. Specifically the following:
        - SNOWSQL_USER
        - SNOWSQL_PWD
        - SNOWSQL_ACCOUNT
        - SNOWSQL_ROLE
        - SNOWSQL_WAREHOUSE
    """

    def open(self, p_query_tag):
        if self.initialized == True:
            return
        try:
            self.logger.info(f"Connecting to snowflake {self.db}.{self.schema} ...")

            self.sqlconn = connector.connect(
                user=os.getenv("SNOWSQL_USER"),
                password=os.getenv("SNOWSQL_PWD"),
                account=os.getenv("SNOWSQL_ACCOUNT"),
                role=os.getenv("SNOWSQL_ROLE"),
                warehouse=os.getenv("SNOWSQL_WAREHOUSE"),
                database=self.db,
                schema=self.schema,
                # Improve Query Performance by Bypassing Data Conversion
                converter_class=SnowflakeNoConverterToPython,
                session_parameters={"QUERY_TAG": p_query_tag},
            )

            self.initialized = True
            self.logger.debug("	sucessfully connected.")

        except snowflake.connector.errors.Error as e:
            logger.error(
                f"Got an error when attempting to open a snowflake connection: '{e}'"
            )
            self.sqlconn = None
            self.initialized = False

        return self.initialized

    """
        Issues query against Snowflake. Support multi-query with each query
        statement seperated by ;. The statement type are rather that performs
        DDL operations like 'create table, create pipe' etc...

        This is not meant to be used for DML based operations like 'INSERT', 'UPDATE'
        or SELECT, as the cursor is not returned to the caller.

        An exception that gets raised will be propagated to the caller.

        Returns the status of Success or Failure. If any of the statements fail
        the status is returned as false.
    """

    def exec_ddl_query(self, p_qry):
        self.logger.debug(f"Executing query {p_qry} ...")

        # Ref : https://docs.snowflake.com/en/user-guide/python-connector-api.html#execute_string
        # NOTE: In general Snowflake recommends running multiple statement query using the 'execute_string'
        # method. Since we are doing deployment scripts which has a need to run multiple statements,
        # we are still proceeding in good faith, that the developer does not do some drastic
        # misuses.
        # Any misuse purely lies on the developer/user of this tool and on how they have the script code
        # implemented.

        # Empty sql statements will result in error being thrown. To avoid
        # this, we remove such empty statements
        sql_qrys_split = p_qry.split(";")
        qrys = [q.strip() for q in sql_qrys_split if len(q.strip()) > 1]

        sql_qrys = ";".join(qrys)

        cursors = self.sqlconn.execute_string(sql_qrys)

        success = False
        for c in cursors:
            query_id = c.sfqid
            # self.logger.info(f" query id : {query_id} ")

            # TODO capture any errors raised by Snowflake, before raising
            # back to the caller, enrich the error with the SQL statement
            # for which the error was raised.
            qry_status = self.sqlconn.get_query_status_throw_if_error(query_id)
            if qry_status == QueryStatus.SUCCESS:
                success = True
            else:
                self.logger.warn(
                    f"QUERY STATUS : {qry_status} \n The statement : \n {p_qry} \n seems to be having issues. "
                )
                succes = False

        return success

    """
        closes the connection with Snowflake.
    """

    def close(self):
        if self.initialized == False:
            return

        try:
            self.sqlconn.close()
            self.sqlconn = None
            self.initialized = False
            self.logger.info("Connection with snowflake is closed")

        except snowflake.connector.errors.Error as e:
            logger.debug(
                f"Got an error when attempting to close the snowflake connection: '{e}'"
            )
            return False

        return True


"""
    Retrieves various metadata information using the INFORMATION_SCHEMA views.
    The queries used to fetch are based of 'dwmr_resources/config/metadata_query.yaml'.
    The retrieved metadata information is stored in the 'work_dir' directory
    as csv files.
"""


class MetadataFetch(SnowflakeConnection):
    def __init__(self, p_config, p_db, p_schema):
        super().__init__(p_db, p_schema)
        self.logger = logging.getLogger("MetadataFetch")
        self.config = p_config
        self.work_dir = self.config["work_dir"].get()

    """
        issues query against view and returns the result 
        as pandas dataframe to the caller.
    """

    def get_df(self, p_qry):
        self.logger.debug(f"Fetching metadata definition ...")
        qry_str = p_qry.format(P_DB=self.db, P_SCHEMA=self.schema)
        self.logger.debug(qry_str)
        cursor = self.sqlconn.cursor()
        cursor.execute(qry_str)
        return cursor.fetch_pandas_all()

    """
        Fetches the metadata, based of the config file 'dwmr_resources/config/metadata_query.yaml' and stores them locally in the work_dir.
    """

    def fetch_and_store_tolocal(self):
        self.logger.info(f"Fetching metadata and storing in {self.work_dir} ...")

        for o in self.config["METADATA_QUERY"]:
            self.logger.info(f" Downloading metadata for {o['TYPE']} ...")
            df = self.get_df(o["QUERY"].get())

            # In case of functions or procedures, the proper way to identify is
            # to have the arguments. Hence we formulate the signature in this step.
            # we cannot do it in sql as it required looping like capabilities
            if o["TYPE"].get() in ["FUNCTION", "PROCEDURE"]:
                df["OBJ_KEY"] = df.apply(
                    lambda x: self.get_function_signature_from_key(x.OBJ_KEY), axis=1
                )
                df["OBJ_NAME"] = df["OBJ_KEY"]

            if (o["TYPE"].get() == "GRANT") and (len(df) > 0):
                df["MOD_OBJ_NAME"] = df.apply(
                    lambda x: self.get_function_signature_from_key(x.OBJ_KEY)
                    if x.GRANT_OBJECT_TYPE in ["FUNCTION", "PROCEDURE"]
                    else x.OBJ_KEY.split("_")[1],
                    axis=1,
                )

            df.to_csv(
                os.path.join(self.work_dir, o["FILE"].get()),
                index=False,
                quoting=csv.QUOTE_NONNUMERIC,
                escapechar="\\",
                encoding="utf-8",
            )

    """
    Used for deriving function signature
    """

    def get_function_signature_from_key(self, p_fn_key):
        fn_sig = p_fn_key.replace("FUNCTION_", "")
        fn_sig = fn_sig.replace("PROCEDURE_", "")
        fn_sig_split = fn_sig.split("::")
        fn_name = fn_sig_split[0]

        arg_types = []
        for fn_args in fn_sig_split[1].split(","):
            x = fn_args.split("-")
            typ = x[len(x) - 1]
            arg_types.append(typ)

        arg_signature = ",".join(arg_types)
        fn_sig = f"{fn_name}({arg_signature})"
        return fn_sig

    """
        For specific objects like tables, we can get the DDL statement as issued or perceived by Snowflake using the get_ddl function. This functions helps us to get the object specific DDL.
    """

    def get_obj_ddl(self, p_objkey, p_objtype, p_objname):
        self.logger.info(f"Fetching ddl for {p_objname} of type {p_objtype} ..")
        ddl_qry_template = self.config["DDL_QUERY"].get()
        qry_str = ddl_qry_template.format(
            OBJ_KEY=p_objkey, OBJ_TYPE=p_objtype, OBJ_NAME=p_objname
        )
        results = self.sqlconn.cursor(DictCursor).execute(qry_str).fetchall()
        return results

    """
        Fetches the ddl for all metadata objects and stores them locally in the
        work_dir as json file.
    """

    def fetch_ddls_and_store_tolocal(self):
        self.logger.info("Fetching ddls for objects ...")

        delta_fl = self.config["PLAN"]["delta_file"].get()
        ddl_fl = self.config["PLAN"]["ddl_file"].get()
        delta_fl_w_path = os.path.join(self.work_dir, delta_fl)
        deltas_df = pd.read_csv(delta_fl_w_path)

        deltas_df = deltas_df[~deltas_df.OBJ_TYPE.isin(["SCRIPT", "#", "GRANT"])]

        ddls = []
        for i, r in deltas_df.iterrows():
            OBJ_TYPE = "TABLE" if r["OBJ_TYPE"] == "BASE_TABLE" else r["OBJ_TYPE"]
            OBJ_NAME = f"{self.db}.{self.schema}.{r['OBJ_NAME']}"
            OBJ_NAME = (
                f"{self.db}.{self.schema}" if r["OBJ_TYPE"] == "SCHEMA" else OBJ_NAME
            )

            ddl_df = self.get_obj_ddl(r["OBJ_KEY"], OBJ_TYPE, OBJ_NAME)
            d = ddl_df[0]
            ddls.append(d)

        self.logger.info(f"Storing retrieved ddls in file : {ddl_fl} ...")
        with open(os.path.join(self.work_dir, ddl_fl), "w") as f:
            json.dump(ddls, f)

        return ddls
