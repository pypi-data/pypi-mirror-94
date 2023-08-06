from .appbase import AppBase
from datetime import datetime
import pandas as pd
import configparser
import re
import logging
import os
import shutil
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

"""
Called specifically during the 'plan' phase, this class main set of action is to
- create a 'plan/plan.csv' based of 'work/delta.csv'
- retain only those scripts which have objects defined in the 'plan/plan.csv'
- filter and transfer the metadata csv files, ex tables.csv, to the plan directory
"""


class PlanPhase(AppBase):
    logger = logging.getLogger("PlanPhase")

    def __init__(self, p_config):
        super().__init__(p_config)
        self.work_dir = self.config["work_dir"].get()
        self.plan_dir = self.config["plan_dir"].get()
        self.plan_file = self.config["plan_file"].get()

    """
    Remove script files which are present in the plan.
    """

    def remove_scripts_notmeant_for_deployment(self, p_plan_df, p_gen_deploy_dir):
        self.logger.info(
            "Removing script files not planned for deployment ...")

        # get the list of files meant for deployment
        deploy_fl_list = p_plan_df["SCRIPT_FILE"].to_list()
        deploy_fl_set = set(deploy_fl_list)

        # get the list of files in gen_dir
        gen_dir = self.config["generated_dir"].get()
        deploy_dir = os.path.join(gen_dir, "deploy")

        # deploy_fl_set.add(os.path.join(deploy_dir, "GRANTS.sql"))

        to_be_deleted = []
        script_files = os.scandir(deploy_dir)
        for fl in script_files:
            fl_w_path = os.path.join(deploy_dir, fl.name)
            script_path = Path(fl_w_path)
            if fl_w_path not in deploy_fl_set:
                self.logger.warn(f" Script file deletion : {fl_w_path}")
                script_path.unlink()
            else:
                # Remove comment lines, the ones that start with '--REM '
                script_txt = script_path.read_text()
                updated_txt = re.sub("--REM.*", "", script_txt)
                # remove empty lines
                updated_txt = re.sub(
                    r"\n\s*\n", "\n", updated_txt, re.MULTILINE)
                script_path.write_text(updated_txt)

    """
    Filter metadata information for specific types, ex TABLES, based of
    whats declared in 'plan.csv'. Once filtered move to plan dir.
    """

    def filter_and_transfer_to_plan_for_object(self, p_df, p_obj_type):
        self.logger.info(f" Filtering and planning for {p_obj_type} types ...")

        # Filter to object specific rows
        delta_df = p_df[p_df.OBJ_TYPE == p_obj_type]

        if p_obj_type == "BASE_TABLE":
            table_view_df = p_df[p_df.OBJ_TYPE == "VIEW"]
            delta_df = pd.concat([delta_df, table_view_df])

        # Load the schema metadata definition
        metadata_fl = self.objtype_to_file_map[p_obj_type]
        obj_meta_df = super().load_df(self.work_dir, metadata_fl)

        delta_obj_df = obj_meta_df.merge(delta_df[["OBJ_KEY"]], on="OBJ_KEY")
        super().save_df(delta_obj_df, self.plan_dir, metadata_fl)

        return delta_obj_df

    """
    Filter tables which has newly added columns or updated data types.
    """

    def filter_columns_for_table(self):
        self.logger.info(f" Migrating columns specific to selected tables ..")

        #        tbl_df = super().load_df(
        #            self.plan_dir, self.objtype_to_file_map["TABLE"])
        #        col_df = super().load_df(
        #            self.work_dir, self.objtype_to_file_map["COLUMN"])
        #
        #        t_df = tbl_df[["OBJ_NAME"]]
        #
        #        delta_col_df = col_df.merge(
        #            t_df, right_on="OBJ_NAME", left_on="TABLE_NAME")
        #        super().save_df(delta_col_df, self.plan_dir,
        #                        self.objtype_to_file_map["COLUMN"])

        work_col_fl_path = os.path.join(
            self.work_dir, "delta_" + self.objtype_to_file_map["COLUMN"]
        )
        plan_col_fl_path = os.path.join(
            self.plan_dir, self.objtype_to_file_map["COLUMN"]
        )
        shutil.copyfile(work_col_fl_path, plan_col_fl_path)

    """
    Generate report based of plan.csv.
    """

    def generate_report(self):
        self.logger.info(f" Generating report ...")

        # Initialize and load the template
        template_dir = self.config["template_dir"].get()
        jinja_env = Environment(loader=FileSystemLoader(template_dir))
        template = jinja_env.get_template("plan_report.md")

        plan_df = super().load_df(self.plan_dir, self.plan_file)
        plan_json = json.loads(plan_df.to_json(orient="records"))
        param = {"plan": plan_json, "report_date": self.EXEC_DATE}
        report = template.render(param)

        plan_report = os.path.join(self.plan_dir, "plan_report.md")
        self.logger.info(f"  report : {plan_report} ")
        plan_fl_path = Path(plan_report)

        plan_fl_path.write_text(report)

    """
    Main entry point.
    """

    def do(self):

        super().delete_and_recreate_dir(self.plan_dir)

        # Load delta file
        delta_fl = self.config["PLAN"]["delta_file"].get()
        delta_df = super().load_df(self.work_dir, delta_fl)
        plan_df = super().reset_execution_order(delta_df)

        # Copy the delta file into the plan dir
        self.logger.info(f"Saving plan file {self.plan_dir}/{self.plan_file} ...")
        super().save_df(plan_df, self.plan_dir, self.plan_file)

        d_df = plan_df[~delta_df.OBJ_TYPE.isin(["SCRIPT", "#"])]

        self.filter_and_transfer_to_plan_for_object(d_df, "SCHEMA")
        self.filter_and_transfer_to_plan_for_object(d_df, "BASE_TABLE")
        self.filter_columns_for_table()
        self.filter_and_transfer_to_plan_for_object(d_df, "FUNCTION")
        self.filter_and_transfer_to_plan_for_object(d_df, "VIEW")
        self.filter_and_transfer_to_plan_for_object(d_df, "PROCEDURE")
        self.filter_and_transfer_to_plan_for_object(d_df, "GRANT")

        self.generate_report()

        gen_dir = self.config["generated_dir"].get()
        self.remove_scripts_notmeant_for_deployment(delta_df, gen_dir)
