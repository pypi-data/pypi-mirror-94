import logging
import os
import configparser
import pandas as pd
from datetime import datetime
from .appbase import AppBase

"""
    Used during the 'init' phase, meant for identifying the list of objects
    that have been changed or newly added. The identified objects are stored
    in 'work/delta.csv'.

    If run multiple times, this will not overwrite previous version of delta.csv. This
    saves from overwriting potential modifications
"""


class DeltaIdentifier(AppBase):
    logger = logging.getLogger(__name__)

    def __init__(self, p_config):
        super().__init__(p_config)
        self.work_dir = self.config["work_dir"].get()
        self.registry_dir = self.config["registry_dir"].get()
        self.delta_fl = self.config["PLAN"]["delta_file"].get()
        self.gen_dir = self.config["generated_dir"].get()

    def save_delta_preserving_earlier_changes(self, p_delta_df, p_delta_fl):
        self.logger.debug(f"Saving identified deltas ...")
        delta_fl_w_path = os.path.join(self.work_dir, p_delta_fl)

        # To avoid overwriting previous delta copy, which might have manual changes
        # we will preserve the existing records and store only new records, if any
        prev_delta_df = super().load_df(self.work_dir, p_delta_fl)

        if prev_delta_df.empty == True:
            super().save_df(p_delta_df, self.work_dir, p_delta_fl)
            return

        (is_new, l_df, r_df, c_df, n_df, m_df, c_md5_df) = super().df_diff(
            prev_delta_df, p_delta_df
        )

        d_df = pd.concat([c_df, m_df])
        d_df = super().reset_execution_order(d_df)

        super().save_df(d_df, self.work_dir, p_delta_fl)

    def enrich(self, p_identified_deltas):
        self.logger.debug(f" Enriching and save deltas ...")

        df = pd.concat(p_identified_deltas)
        df = df[
            [
                "OBJ_TYPE",
                "OBJ_NAME",
                "OBJ_KEY",
                "OBJ_MD5",
                "DETECTION",
                "DEPLOY_STRATEGY",
                "DELTA_COMMENT",
            ]
        ]

        # set this to avoid the 'SettingWithCopyWarning' message2
        pd.set_option("mode.chained_assignment", None)

        # Create this dummy call to avoid error on the below lambda
        df["SCRIPT_FILE"] = ""
        df["SCRIPT_FILE"] = df.apply(
            lambda x: os.path.join(self.gen_dir, "deploy", x.OBJ_KEY + ".sql"), axis=1
        )
        df["VERIFY_FILE"] = ""
        df["VERIFY_FILE"] = df.apply(
            lambda x: os.path.join(self.gen_dir, "verify", x.OBJ_KEY + ".sql"), axis=1
        )
        df["REVERT_FILE"] = ""
        df["REVERT_FILE"] = df.apply(
            lambda x: os.path.join(self.gen_dir, "revert", x.OBJ_KEY + ".sql"), axis=1
        )
        df["DEPLOYMENT_ROLE"] = "-"

        # In case of GRANT, all grant statements are defined in a single GRANT FILE
        # Hence reset script file to same for rows whose obj type is GRANT
        df["SCRIPT_FILE"] = df.apply(
            lambda x: os.path.join(self.gen_dir, "deploy", "GRANTS.sql")
            if x.OBJ_TYPE == "GRANT"
            else x.SCRIPT_FILE,
            axis=1,
        )
        d_df = df.drop_duplicates("OBJ_KEY")
        # reset
        pd.set_option("mode.chained_assignment", "raise")

        d_df = super().reset_execution_order(d_df)
        return d_df

    def identify_deltas_on_various_objects(self):
        obj2fl_map = self.objtype_to_file_map.copy()
        obj2fl_map.pop("COLUMN", "")
        obj2fl_map.pop("VIEW", "")
        obj2fl_map.pop("BASE_TABLE", "")

        delta_df_list = []
        for obj_type, meta_fl in obj2fl_map.items():
            self.logger.info(f" Identifying delta on type {obj_type} ...")
            (
                is_new,
                l_df,
                r_df,
                c_df,
                new_objs_df,
                dropped_objs_df,
                altered_c_df,
            ) = super().load_metadata_and_diff(
                self.work_dir, self.registry_dir, meta_fl
            )

            if is_new:
                l_df["DETECTION"] = "A"
                l_df["DEPLOY_STRATEGY"] = "CREATE"
                l_df["DELTA_COMMENT"] = "new run."
                delta_df_list.append(l_df)

            if new_objs_df is not None:
                new_objs_df["DETECTION"] = "A"
                new_objs_df["DEPLOY_STRATEGY"] = "CREATE"
                new_objs_df["DELTA_COMMENT"] = "newly addded tables"
                delta_df_list.append(new_objs_df)

            if altered_c_df is not None:
                altered_c_df["DETECTION"] = "U"
                altered_c_df["DEPLOY_STRATEGY"] = "ALTER"
                altered_c_df["DELTA_COMMENT"] = "change in table attributes."
                delta_df_list.append(altered_c_df)

        return delta_df_list

    """
    Tables that were deployed earlier could have been modified due to 
    - new column added
    - existing column but thier data type is changed
    - columns getting dropped.

    This function is used for identifying such tables that have been modified
    due to the column deltas.
    """

    def identify_tables_altered_basedof_col_saveto_delta(self):

        column_meta_fl = self.objtype_to_file_map["COLUMN"]
        delta_col_meta_fl = "delta_" + column_meta_fl

        tbl_df = super().load_df(self.work_dir, self.objtype_to_file_map["TABLE"])
        delta_col_df = super().load_df(self.work_dir, delta_col_meta_fl)

        delta_col_df = delta_col_df[["TABLE_NAME"]].drop_duplicates()
        t_df = tbl_df.merge(
            delta_col_df[["TABLE_NAME"]],
            left_on="OBJ_NAME",
            right_on="TABLE_NAME",
            how="inner",
        )

        t_df["DETECTION"] = "U"
        t_df["DEPLOY_STRATEGY"] = "ALTER"
        t_df["DELTA_COMMENT"] = "new columns present"

        return t_df

    """
    Used for identifying and filtering columns that are newly added or modified from
    previous deployment runs.
    """

    def identify_and_save_delta_columns(self):
        # Identify columns that were added/dropped/modified and retain only those
        column_meta_fl = self.objtype_to_file_map["COLUMN"]

        (
            is_new_col_obj,
            l_df,
            r_df,
            common_df,
            new_col_df,
            dropped_df,
            altered_c_df,
        ) = super().load_metadata_and_diff(
            self.work_dir, self.registry_dir, column_meta_fl
        )

        d_col_df = l_df if is_new_col_obj == True else new_col_df
        self.save_delta_preserving_earlier_changes(d_col_df, "delta_" + column_meta_fl)

    """
    Main entry point to perform action.
    """

    def do(self, p_db, p_schema):
        delta_df_list = self.identify_deltas_on_various_objects()

        self.identify_and_save_delta_columns()
        tables_altered_by_cols = self.identify_tables_altered_basedof_col_saveto_delta()

        delta_df_list.append(tables_altered_by_cols)

        enriched_df = self.enrich(delta_df_list)
        self.save_delta_preserving_earlier_changes(enriched_df, self.delta_fl)
