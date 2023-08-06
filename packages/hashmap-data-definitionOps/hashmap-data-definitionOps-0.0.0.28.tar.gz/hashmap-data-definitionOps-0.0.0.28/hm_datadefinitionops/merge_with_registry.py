import logging
import os
from pathlib import Path
import configparser
import pandas as pd
from datetime import datetime
from .appbase import AppBase


"""
This is called during the 'init' phase, the goal being to migrate metadata found
in 'plan' to be merged with the corresponding metadata in the 'registry' folder.
And also for clarification reasons, get the DDL into 'registry/deploy' folder.
"""


class RegistryMerger(AppBase):
    logger = logging.getLogger("RegistryMerger")

    def __init__(self, p_config):
        super().__init__(p_config)
        self.work_dir = self.config["work_dir"].get()
        self.plan_dir = self.config["plan_dir"].get()
        self.registry_dir = self.config["registry_dir"].get()

    """
    Merges the scripts found in the generated into existing script with the
    same name in 'registry/deploy'. The main reason is to keep track.
    """

    def merge_script(self, p_from_script_dir, p_to_script_dir):
        self.logger.info(
            f" Merging scripts from {p_from_script_dir} into {p_to_script_dir} ..."
        )

        to_be_deleted = []
        script_files = os.scandir(p_from_script_dir)
        for fl in script_files:
            to_fl_w_path = os.path.join(p_to_script_dir, fl.name)
            from_fl_w_path = os.path.join(p_from_script_dir, fl.name)

            sql_text = Path(from_fl_w_path).read_text()

            merge_or_add = "Merge" if (
                os.path.exists(to_fl_w_path) == True) else "Add"
            self.logger.info(f"   {fl.name} : {merge_or_add} ")

            with open(to_fl_w_path, "a") as f:
                f.write("\n\n ------------------ \n\n")
                f.write(sql_text)

                # Remove only on successful writes
                os.remove(from_fl_w_path)

        # For any files not found in the destination folder, just move them

    def rename_and_back_plan(self):
        plan_file = self.config["plan_file"].get()
        reg_deploy_dir = os.path.join(self.registry_dir, 'deploy')
        old_plan_file = os.path.join(self.plan_dir, plan_file)
        new_plan_file = os.path.join(reg_deploy_dir, f'{plan_file}_{self.EXEC_DATE}')
        self.logger.info(f' backing up plan file as : {new_plan_file} ...')
        os.rename(old_plan_file, new_plan_file)

    """
    Main entry point.
    """

    def do(self):

        super().delete_and_recreate_dir(self.work_dir)

        gen_dir = self.config["generated_dir"].get()
        for sub_dir in ["deploy"]:  # TODO include revert & verify later releases
            from_dir = os.path.join(gen_dir, sub_dir)
            to_dir = os.path.join(self.registry_dir, sub_dir)
            self.merge_script(from_dir, to_dir)

        for k, v in self.objtype_to_file_map.items():
            if (
                k == "BASE_TABLE"
            ):  # This is a double entry to table. hence ignore this key
                continue

            if os.path.exists(os.path.join(self.plan_dir, v)) == False:
                self.logger.warn(
                    f" {os.path.join(self.plan_dir, v)} does not exist, skipping merge to registry. "
                )
                continue

            (
                is_new,
                deployed_df,
                reg_df,
                common_df,
                new_df,
                dropped_df,
                altered_c_df,
            ) = super().load_metadata_and_diff(self.plan_dir, self.registry_dir, v)

            if is_new == True:
                super().save_df(deployed_df, self.registry_dir, v)
            else:
                # Add newly added objects
                reg_w_deployed = pd.concat([reg_df, new_df])

                # For objects which differ in check sum, update the checksum field
                t_df = reg_w_deployed.loc[
                    ~(reg_w_deployed.OBJ_KEY.isin(altered_c_df["OBJ_KEY"])), :
                ]
                registry_updated_df = pd.concat([t_df, altered_c_df])

                super().save_df(registry_updated_df, self.registry_dir, v)

            os.remove(os.path.join(self.plan_dir, v))

        self.rename_and_back_plan()
