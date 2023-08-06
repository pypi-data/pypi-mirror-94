import pytest
import confuse
import os
from pathlib import Path
import pandas as pd
import json
from hm_datadefinitionops.delta_identifier import DeltaIdentifier


@pytest.fixture
def delta_identifier(config):
    return DeltaIdentifier(config)


def test_enrich(delta_identifier):

    d_df_dict = [
        {
            "OBJ_TYPE": "GRANT",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "GR_TB_01",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        }
    ]
    d_df = pd.read_json(json.dumps(d_df_dict), orient="records")

    e_df = delta_identifier.enrich([d_df])
    script = e_df.iloc[0]["SCRIPT_FILE"]
    assert script == "generated/deploy/GRANTS.sql"


def test_save_delta_preserving_earlier_changes_new(delta_identifier):

    d_df_dict = [
        {
            "OBJ_TYPE": "PRE_SCRIPT",
            "OBJ_NAME": "PRE",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "PRE",
        }
    ]
    d_df = pd.read_json(json.dumps(d_df_dict), orient="records")

    delta_identifier.save_delta_preserving_earlier_changes(d_df, "delta.csv")


def test_save_delta_preserving_earlier_changes_preserve(delta_identifier):

    # Create older record
    old_df_dict = [
        # This record will be common between both
        {
            "OBJ_TYPE": "PRE_SCRIPT",
            "OBJ_NAME": "PRE",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "PRE",
        },
        # This record will be dropped in the new df
        {"OBJ_TYPE": "SCHEMA", "OBJ_NAME": "SCH", "OBJ_MD5": "7777", "OBJ_KEY": "SCH"},
        # This record will be present in both, however the value is modified
        {"OBJ_TYPE": "TABLE", "OBJ_NAME": "TBL", "OBJ_MD5": "9999", "OBJ_KEY": "TBL"},
    ]
    old_df = pd.read_json(json.dumps(old_df_dict), orient="records")
    delta_identifier.save_df(old_df, "work", "delta.csv")

    new_df_dict = [
        # This record will be common between both
        {
            "OBJ_TYPE": "PRE_SCRIPT",
            "OBJ_NAME": "PRE",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "PRE",
        },
        # This record is new
        {"OBJ_TYPE": "PIPE", "OBJ_NAME": "PIP", "OBJ_MD5": "3333", "OBJ_KEY": "PIPES"},
        # This record will be present in both, however the value is modified
        {"OBJ_TYPE": "TABLE", "OBJ_NAME": "TBL", "OBJ_MD5": "5555", "OBJ_KEY": "TBL"},
    ]
    new_df = pd.read_json(json.dumps(new_df_dict), orient="records")

    delta_identifier.save_delta_preserving_earlier_changes(new_df, "delta.csv")

    s_df = delta_identifier.load_df("work", "delta.csv")

    md5_list = s_df["OBJ_MD5"].to_list()

    assert ("9999" in md5_list) == True  # ensure modified record is preserved
    # ensure record not present in the new one is dropped
    assert ("7777" in md5_list) == False
    # ensure records that are common are present
    assert ("b749d" in md5_list) == True
    assert ("3333" in md5_list) == True  # ensure new records are added

    assert ("5555" in md5_list) == False
