import pytest
import logging
import os
import confuse
import glob
from pathlib import Path
from importlib import resources

"""
Create base project setup.
"""


@pytest.fixture(scope="session", autouse=True)
def project_setup(tmp_path_factory):
    tmpdir = tmp_path_factory.getbasetemp()
    cwd = os.getcwd()

    gen_dir = "generated"
    registry_dir = "registry"
    plan_dir = "plan"
    templates_dir = "templates"
    for d in [
        templates_dir,
        "work",
        plan_dir,
        registry_dir,
        gen_dir,
        os.path.join(gen_dir, "deploy"),
        os.path.join(gen_dir, "verify"),
        os.path.join(gen_dir, "revert"),
        os.path.join(plan_dir, "deploy"),
        os.path.join(plan_dir, "verify"),
        os.path.join(plan_dir, "revert"),
        os.path.join(registry_dir, "deploy"),
    ]:
        dr = os.path.join(tmpdir, d)
        os.makedirs(dr, exist_ok=True)

    fl_content = resources.read_text("hmddops_resources.config", "config.yaml")
    Path(os.path.join(tmpdir, "config_default.yaml")).write_text(fl_content)

    with resources.path("hmddops_resources", "templates") as p:
        for c in p.iterdir():
            script_fl = Path(os.path.join(tmpdir, templates_dir, c.name))
            script_fl.write_text(c.read_text())

    os.chdir(tmpdir)


@pytest.fixture(autouse=True)
def config():
    print("ASDA")
    print("Test project base dir : " + os.getcwd())
    APP_NAME = os.path.basename("dwmetareplicate_snowflake")
    config = confuse.Configuration(APP_NAME, __name__)

    # Load from project root directory. Assumption we are
    # operating from the project root
    config.set_file(os.path.join(os.getcwd(), "config_default.yaml"))

    metadata_query_fl = resources.path(
        "hmddops_resources.config", "metadata_query.yaml"
    )
    with resources.path("hmddops_resources.config", "metadata_query.yaml") as p:
        config.set_file(p.resolve())

    return config


@pytest.fixture(autouse=True)
def cleanup_dir():
    print("Cleaning up files in directories.")
    cwd = os.getcwd
    files = glob.glob(os.path.join(os.getcwd(), "*.csv"), recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print(f"	Unable to delete file : {f}, {e.strerror}")
