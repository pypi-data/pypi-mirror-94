import logging
import os
import configparser
import pandas as pd
from datetime import datetime
from .appbase import AppBase
from jinja2 import Template
from pathlib import Path

"""
Used during the 'apply' phase, this class main goal is to execute the various script
against the target database and schema in specific sequence.

You also run this class under a 'dry-run' where by the scripts get configured and created
for the target db/schema but does not get executed.
"""


class ApplyPhase(AppBase):
    logger = logging.getLogger("ApplyPhase")

    def __init__(self, p_config, p_db, p_schema):
        super().__init__(p_config)
        self.db = p_db
        self.schema = p_schema
        self.work_dir = self.config["work_dir"].get()
        self.registry_dir = self.config["registry_dir"].get()
        self.delta_fl = self.config["PLAN"]["delta_file"].get()
        self.plan_dir = self.config["plan_dir"].get()
        self.plan_file = self.config["plan_file"].get()
        self.gen_dir = self.config["generated_dir"].get()

    """
    Jinja templates would sometime have a need to reference specific environmental
    variables, example SNOWSQL_DATABASE. In such cases we need to retrieve these
    environmental variables and pass it down the script.

    This function is used to retrieve specific set of environment variables and create
    a dictionary, which is used to sent to the script under the template variable os_env.

    The list of environment variables to retrieve are found in the APPLY/ENV section.
    """

    def get_env_var_dict(self):
        # parse the ENV and pass to the template rendering
        env_list = self.config["APPLY"]["ENV"].get()
        param_env = {}
        for env in env_list:
            e = os.getenv(env, "--NOT SET IN ENV--")
            param_env[env] = e

        return param_env

    """
    This script substitute target environment specific replacements in the
    script and creates the final script which will then be called upon.
    """

    def detemplitize_script(self, p_script_file):
        sql_txt = ""
        with open(p_script_file, "r") as f:
            sql_txt = f.read()

        target = {"DB": self.db, "SCH": self.schema}
        # parse the ENV and pass to the template rendering
        param_env = self.get_env_var_dict()

        # parse the KEYWORD_MAP and pass to the template rendering
        keyword_map = self.config["APPLY"]["KEYWORD_MAP"].get()

        render_param = {}
        render_param["os_env"] = param_env
        render_param["keyword_map"] = keyword_map
        render_param["target"] = target
        sql_qry_txt = Template(sql_txt).render(render_param)
        self.logger.debug(sql_qry_txt)

        return sql_qry_txt

    """
    Execute the script for a specific object types.
    """

    def exec_scripts_for_type(self, p_plan_df, p_snow_conn):
        t_df = p_plan_df
        default_role = os.environ.get("SNOWSQL_ROLE")

        if t_df.empty == True:
            return

        previously_ran = set()
        for i, row in t_df.iterrows():
            script = row["SCRIPT_FILE"]

            if script in previously_ran:
                continue

            previously_ran.add(script)
            sql_qry_txt = self.detemplitize_script(script)

            # TODO Handle deployment_strategy
            # TODO change to role reflected in 'DEPLOYMENT_ROLE'
            deploy_role = (
                row["DEPLOYMENT_ROLE"]
                if row["DEPLOYMENT_ROLE"] != "-"
                else default_role
            )
            # role_stmt = f'use role {deploy_role}; '
            self.logger.info(f"   Executing script: {script} ...")

            sql_qry_txt = f"use role {deploy_role};\n" + sql_qry_txt

            p_snow_conn.exec_ddl_query(sql_qry_txt)

    """
    Main entry point
    """

    def do(self, p_snow_conn, p_dry_run_only):

        super().delete_and_recreate_dir(self.work_dir)

        plan_df = super().load_df(self.plan_dir, self.plan_file)

        self.dry_run()

        if p_dry_run_only == False:
            self.exec_scripts_for_type(plan_df, p_snow_conn)

    """
    Perform dry run, which is just to create the script.
    """

    def dry_run(self):
        self.logger.info(
            f" Generating scripts for the target database and schema. {self.db}.{self.schema} ..."
        )
        plan_df = super().load_df(self.plan_dir, self.plan_file)
        default_role = os.environ.get("SNOWSQL_ROLE")

        dry_run_dir = os.path.join(self.work_dir, "dry_run")
        os.makedirs(dry_run_dir, exist_ok=True)
        self.logger.info(f" Generated script files will be in folder : {dry_run_dir} ")

        previously_ran = set()
        for k, row in plan_df.iterrows():
            deploy_role = (
                row["DEPLOYMENT_ROLE"]
                if row["DEPLOYMENT_ROLE"] != "-"
                else default_role
            )
            script = row["SCRIPT_FILE"]

            if script in previously_ran:
                continue

            previously_ran.add(script)

            sql_qry_txt = self.detemplitize_script(script)

            sql_qry_txt = f"use role {deploy_role};\n" + sql_qry_txt
            idx = int(row["EXECUTION_ORDER"])

            script_fl_name = script.split("/")[2]
            dry_run_script = os.path.join(dry_run_dir, f"_{idx:03d}_{script_fl_name}")
            self.logger.info(f"  File : {dry_run_script} ")

            Path(dry_run_script).write_text(sql_qry_txt)
