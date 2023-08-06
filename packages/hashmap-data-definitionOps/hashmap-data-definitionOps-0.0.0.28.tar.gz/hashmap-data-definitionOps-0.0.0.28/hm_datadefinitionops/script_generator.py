import logging
import logging
import os
import json
import configparser
import pandas as pd
from datetime import datetime
from .appbase import AppBase
from jinja2 import Environment, FileSystemLoader

"""
Used for generating scripts, based of various objects found in the delta.

The jinja template script would be present in the 'templates' directory.
"""


class ScriptGenerator(AppBase):
    logger = logging.getLogger("ScriptGenerator")

    def __init__(self, p_config):
        super().__init__(p_config)
        self.work_dir = self.config["work_dir"].get()
        self.template_dir = self.config["template_dir"].get()
        self.jinja_env = Environment(loader=FileSystemLoader(self.template_dir))

    """
    In the current implementation, grants statements across various objects are
    collectively stored in a specific 'GRANTS.csv' file. the creation process is 
    a little bit different in comparison to other DB objects. Hence this script
    is defined specifically for grants.
    """

    def generate_script_for_grant(self):
        self.logger.info(f" Generating scripts for grants ...")
        # Script for grant objects
        grant_df = super().load_df(
            self.work_dir, self.config["PLAN"]["delta_file"].get()
        )
        # Filter to only grants
        grant_df = grant_df[grant_df.OBJ_TYPE == "GRANT"]

        if grant_df.empty:
            self.logger.warn(
                " **************  THERE IS NO GRANT SPECIFIC. NO SCRIPTS GENERATED ****"
            )
            return

        obj_type = "GRANT"

        # load the template
        self.template = self.jinja_env.get_template("grants.sql")

        # drop these columns as they will get sourced from meta df
        grant_df = grant_df.drop(["OBJ_NAME", "OBJ_TYPE"], axis=1)

        # Load the object metadata definition
        obj_meta_df = super().load_df(self.work_dir, self.objtype_to_file_map[obj_type])

        delta_obj_df = obj_meta_df.merge(grant_df, on="OBJ_KEY")

        render_param = {}
        render_param["GENERATE_DATE"] = self.EXEC_DATE
        grants_dict = json.loads(delta_obj_df.to_json(orient="records"))
        render_param["grants"] = grants_dict

        sql_script = self.template.render(render_param)
        gen_dir = self.config["generated_dir"].get()

        script_fl = grants_dict[0]["SCRIPT_FILE"]
        with open(script_fl, "w") as f:
            f.write(sql_script)

    """
    Generate scripts for all non grants related DW objects. The generated script
    will be stored in 'generated' dir.
    """

    def generate_script_for_object(self, p_df, p_obj_type, p_template_fl):
        self.logger.info(f" Generating for {p_obj_type} types ...")

        # load the template
        self.template = self.jinja_env.get_template(p_template_fl)

        # Filter to object specific rows
        delta_df = p_df[p_df.OBJ_TYPE == p_obj_type]

        # drop these columns as they will get sourced from meta df
        delta_df = delta_df.drop(["OBJ_NAME", "OBJ_TYPE"], axis=1)

        # Load the object metadata definition
        obj_meta_df = super().load_df(
            self.work_dir, self.objtype_to_file_map[p_obj_type]
        )

        delta_obj_df = obj_meta_df.merge(delta_df, on="OBJ_KEY")

        if p_obj_type == "SCHEMA":
            delta_obj_df["DDL"] = delta_obj_df["DDL_DEFN"]

        # not all objects have the DDL_DEFN
        if "DDL_DEFN" in delta_obj_df:
            delta_obj_df = delta_obj_df.drop(["DDL_DEFN"], axis=1)

        delta_col_df = None
        if p_obj_type == "BASE_TABLE":
            delta_col_df = super().load_df(
                self.work_dir, "delta_" + self.objtype_to_file_map["COLUMN"]
            )
            delta_col_df = delta_col_df[
                [
                    "TABLE_NAME",
                    "OBJ_NAME",
                    "COLUMN_DEFAULT",
                    "IS_NULLABLE",
                    "DATA_TYPE",
                    "COMMENT",
                    "OBJ_KEY",
                ]
            ]

        for index, row in delta_obj_df.iterrows():

            render_param = {}
            render_param["ddl"] = row

            # Add the columns to the row in case of table
            if (p_obj_type == "BASE_TABLE") and (row["DETECTION"] != "A"):
                col_df = delta_col_df[delta_col_df.TABLE_NAME == row["OBJ_NAME"]]
                col_df = col_df.drop(["TABLE_NAME"], axis=1)
                col_dict = json.loads(col_df.to_json(orient="records"))
                render_param["cols"] = col_dict

            sql_script = self.template.render(render_param)
            with open(row["SCRIPT_FILE"], "w") as f:
                f.write(sql_script)

    """
    Main entry point.
    """

    def do(self):
        gen_dir = self.config["generated_dir"].get()

        # Load delta file
        delta_df = super().load_df(
            self.work_dir, self.config["PLAN"]["delta_file"].get()
        )
        delta_df = delta_df[~delta_df.OBJ_TYPE.isin(["SCRIPT", "#", "GRANT"])]

        if delta_df.empty:
            self.logger.warn(
                " **************  THERE IS NO OBJECT SPECIFIC SCRIPTS TO DEPLOY. NO SCRIPTS GENERATED ****"
            )
            self.generate_script_for_grant()
            return

        ddl_fl_w_path = os.path.join(
            self.work_dir, self.config["PLAN"]["ddl_file"].get()
        )
        ddl_df = pd.read_json(ddl_fl_w_path)

        d_df = delta_df.merge(ddl_df, on="OBJ_KEY")
        d_df["GENERATE_DATE"] = self.EXEC_DATE

        self.generate_script_for_object(d_df, "SCHEMA", "schema.sql")
        self.generate_script_for_object(d_df, "BASE_TABLE", "table.sql")
        self.generate_script_for_object(d_df, "VIEW", "generic.sql")
        self.generate_script_for_object(d_df, "FUNCTION", "generic.sql")
        self.generate_script_for_object(d_df, "PROCEDURE", "generic.sql")

        self.generate_script_for_grant()
