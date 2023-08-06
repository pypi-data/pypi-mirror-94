import pytest
import confuse
import os
from pathlib import Path
import pandas as pd
import json
from hm_datadefinitionops.appbase import AppBase


@pytest.fixture
def appBase(config):
    return AppBase(config)


def test_df_diff_new(appBase):

    l_df_dict = [
        {
            "OBJ_TYPE": "SCHEMA",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "SCHEMA_GITHUB",
        }
    ]
    r_df_dict = None
    l_df = pd.read_json(json.dumps(l_df_dict), orient="records")
    r_df = pd.read_json(json.dumps(r_df_dict), orient="records")

    (is_new, r_l_df, r_r_df, c_df, n_df, m_df, md5_df) = appBase.df_diff(l_df, r_df)


def test_df_diff_previous_exists(appBase):

    l_df_dict = [
        {
            "OBJ_TYPE": "SCHEMA",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "SCHEMA_GITHUB",
        }
    ]
    r_df_dict = [
        {
            "OBJ_TYPE": "SCHEMA",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "SCHEMA_GITHUB",
        }
    ]
    l_df = pd.read_json(json.dumps(l_df_dict), orient="records")
    r_df = pd.read_json(json.dumps(r_df_dict), orient="records")

    (is_new, r_l_df, r_r_df, c_df, n_df, m_df, md5_df) = appBase.df_diff(l_df, r_df)

    assert is_new == False
    assert len(c_df) == 1
    assert n_df.empty == True
    assert m_df.empty == True
    assert md5_df.empty == True


def test_df_diff_all(appBase):

    l_df_dict = [
        {"OBJ_KEY": "C", "OBJ_MD5": "b749d"},  # common record
        {"OBJ_KEY": "CMD5", "OBJ_MD5": "nnnn"},  # common record but md5 differs
        {"OBJ_KEY": "NEW", "OBJ_MD5": "0000"},  # new record
    ]
    r_df_dict = [
        {"OBJ_KEY": "C", "OBJ_MD5": "b749d"},
        {"OBJ_KEY": "CMD5", "OBJ_MD5": "llll"},
        # old record that is not present in the other
        {"OBJ_KEY": "OLD", "OBJ_MD5": "6666"},
    ]
    l_df = pd.read_json(json.dumps(l_df_dict), orient="records")
    r_df = pd.read_json(json.dumps(r_df_dict), orient="records")

    (is_new, r_l_df, r_r_df, c_df, n_df, m_df, md5_df) = appBase.df_diff(l_df, r_df)

    assert is_new == False
    assert c_df.empty == False
    assert c_df.iloc[0]["OBJ_KEY"] == "C"
    assert md5_df.empty == False
    assert md5_df.iloc[0]["OBJ_MD5"] == "nnnn"

    assert n_df.empty == False
    assert n_df.iloc[0]["OBJ_KEY"] == "NEW"

    assert m_df.empty == False
    assert m_df.iloc[0]["OBJ_KEY"] == "OLD"


def test_reset_execution_order(appBase):

    d_df_dict = [
        {
            "OBJ_TYPE": "SCRIPT",
            "OBJ_NAME": "PRE",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "PRE",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        },
        {
            "OBJ_TYPE": "TABLE",
            "OBJ_NAME": "CMT",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "TABLE",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        },
        {
            "OBJ_TYPE": "VIEW",
            "OBJ_NAME": "PUSH",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "VIEW",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        },
        {
            "OBJ_TYPE": "PIPE",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "PIPE",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        },
        {
            "OBJ_TYPE": "SCHEMA",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "SCHEMA",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        },
        {
            "OBJ_TYPE": "GRANT",
            "OBJ_NAME": "GITHUB",
            "OBJ_MD5": "b749d",
            "OBJ_KEY": "GR_TB_01",
            "DETECTION": "A",
            "DEPLOY_STRATEGY": "CREATE",
            "DELTA_COMMENT": "new",
        },
    ]
    d_df = pd.read_json(json.dumps(d_df_dict), orient="records")

    e_df = appBase.reset_execution_order(d_df)

    expected_exec_order = {
        "SCRIPT": 10,
        "SCHEMA": 20,
        "TABLE": 30,
        "VIEW": 40,
        "PIPE": 50,
        "GRANT": 60,
    }

    # Ensure sort order
    for i in range(1, len(d_df) - 1):
        exec_order = e_df.iloc[i]["EXECUTION_ORDER"]
        obj_type = e_df.iloc[i]["OBJ_TYPE"]
        assert expected_exec_order[obj_type] == exec_order
