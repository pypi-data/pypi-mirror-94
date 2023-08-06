import logging
import os
import csv
import configparser
import pandas as pd
from datetime import datetime
from pathlib import Path
import shutil

"""
    Application base class that is mainly used for defining common functionalities.
"""


class AppBase:
    logger = logging.getLogger("AppBase")
    EXEC_DATE_TIME = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    EXEC_DATE = datetime.now().strftime("%Y-%m-%d")

    # Map that defines the relation between DBobject (ex: SCHEMA) with the
    # metadata file (schema.csv). The relation is based of whats been defined
    # in the file 'dwmr_resources/config/metadata_query.yaml'.
    objtype_to_file_map = {}

    def __init__(self, p_config):
        self.config = p_config
        self.build_objtype_to_file_map()

    """
        Initilizes the class level variable objtype_to_file_map, which holds the
        relation between the DB object to its metadata file.
    """

    def build_objtype_to_file_map(self):
        for o in self.config["METADATA_QUERY"]:
            self.objtype_to_file_map[o["TYPE"].get()] = o["FILE"].get()
        self.objtype_to_file_map["BASE_TABLE"] = self.objtype_to_file_map["TABLE"]

    """
    Saves a dataframe to a specific file. Example usage is to store the 'plan.csv' file,
    which identifies the list of objects that are to be deployed.
    """

    def save_df(self, p_df, p_dir, p_flname):
        dest_fl = os.path.join(p_dir, p_flname)
        self.logger.debug(f" Saving to file {dest_fl} ...")
        p_df.to_csv(
            dest_fl,
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar="\\",
            encoding="utf-8",
        )

    """
    Loads a metadata file and returns it as a dataframe.
    """

    def load_df(self, p_dir, p_flname):
        metadata_fl = os.path.join(p_dir, p_flname)
        self.logger.debug(f" Loading file : {metadata_fl} ...")
        df = pd.DataFrame()

        if os.path.isfile(metadata_fl):
            if os.path.getsize(metadata_fl) > 1:
                df = pd.read_csv(metadata_fl)
        else:
            self.logger.warning(f"No file found : {metadata_fl}")
            # TODO raise an exception

        return df

    """
    Used for differenting 2 dataframe, which holds metadata info. Example usage
    is to compare, difference between what has been deployed previously with what is
    yet to be deployed during the init phase.
    """

    def df_diff(self, l_df, r_df):
        if r_df.empty:
            self.logger.debug("  The right dataframe is empty .")
            return (True, l_df, r_df, None, None, None, None)

        # TODO improve or change this using just outer based join and
        # avoid this specific join based approach.

        # records that are common
        c_df = l_df.merge(r_df[["OBJ_KEY"]], on="OBJ_KEY", how="inner")
        # c_df = c_df.drop(['_merge'], axis=1)

        # identify records that are common based of OBJ_KEY but are differed by MD5
        c_md5_df = c_df.merge(
            r_df[["OBJ_MD5"]],
            on=["OBJ_MD5"],
            suffixes=("", "_y"),
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only"]
        c_md5_df = c_md5_df.drop(["_merge"], axis=1)

        # Newly found objects
        n_df = l_df.merge(
            r_df[["OBJ_KEY"]], on="OBJ_KEY", how="outer", indicator=True
        ).loc[lambda x: x["_merge"] == "left_only"]
        n_df = n_df.drop(["_merge"], axis=1)

        # Records from prev, which could have been added manually
        m_df = r_df.merge(
            l_df[["OBJ_KEY"]], on="OBJ_KEY", how="outer", indicator=True
        ).loc[lambda x: x["_merge"] == "left_only"]
        m_df = m_df.drop(["_merge"], axis=1)

        return (False, l_df, r_df, c_df, n_df, m_df, c_md5_df)

    """
        For a given object like SCHEMA, load metadata file ('schema.csv') from
        multiple directories (work_dir, registry_dir) and return the difference
        back to the caller.
    """

    def load_metadata_and_diff(self, p_left_dir, p_right_dir, p_meta_fl):
        r_df = self.load_df(p_right_dir, p_meta_fl)
        l_df = self.load_df(p_left_dir, p_meta_fl)

        return self.df_diff(l_df, r_df)

    def reset_execution_order(self, p_df):
        # Reshuffling might be needed

        d_df = p_df
        if "EXECUTION_ORDER" in d_df.columns:
            d_df = d_df.drop(["EXECUTION_ORDER"], axis=1)

        OBJECT_TYPE_SORT_DICT = self.config["OBJECT_TYPE_SORT_ORDER"].get()
        d_df = d_df.sort_values(
            by=["OBJ_TYPE"], key=lambda x: x.map(OBJECT_TYPE_SORT_DICT)
        )

        # Insert a execution order column which is meant to specify
        # the order in which the script should be run
        d_df.insert(0, "EXECUTION_ORDER", [
                    i * 10 for i in range(1, len(d_df) + 1)])

        d_df.reset_index(inplace=True)
        d_df = d_df.drop(["index"], axis=1)

        return d_df

    """
    Used for deletion of directories recurively and recreate it.
    """

    def delete_and_recreate_dir(self, p_dir):
        self.logger.debug(f'Deleting and recreating {p_dir} ...')

        p_path = Path(p_dir)
        if p_path.exists():
            shutil.rmtree(p_dir)
        os.makedirs(p_dir, exist_ok=True)
