"""
    This is the main entry point class for the Hashmap DataDefinitionOps.
"""
import sys
import argparse
import confuse
import logging
import os
from pathlib import Path
from importlib import resources
from .snowconnection import MetadataFetch
from .delta_identifier import DeltaIdentifier
from .script_generator import ScriptGenerator
from .plan_phase import PlanPhase
from .apply_phase import ApplyPhase
from .merge_with_registry import RegistryMerger

APP_NAME = os.path.basename(os.getcwd())
config = confuse.Configuration(APP_NAME, __name__)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def parse_arg():
    parser = argparse.ArgumentParser(
        prog="Hasmap DataDefinitionOps",
        description="An alternative approach for performing database devops. This implementation for Snowflake datawarehouse.",
    )
    parser.add_argument("-c", "--config", action="append",
                        help="configuration file.")
    parser.add_argument("-l", "--loglevel", help="log level", default="INFO")
    parser.add_argument(
        "-d",
        "--dryrun",
        help="during apply phase this option creates the script specific to the target db & schema but will not actually create on the target.",
        action="store_true",
    )
    parser.add_argument(
        "-w",
        "--work_dir",
        help="work directory where various downloaded artifacts are stored.",
        default="work",
    )
    parser.add_argument(
        "operation",
        help="the type of operation to perform.",
        metavar="OPERATION",
        choices=["create", "import", "plan", "apply", "merge"],
    )
    args = parser.parse_args()
    config.set_args(args, dots=True)
    return args


def setloglevel(p_loglevel, p_args):
    numeric_level = getattr(logging, p_loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % loglevel)
    print("log level {}  => {}".format(p_args.loglevel, numeric_level))
    logging.basicConfig(level=numeric_level)
    logging.getLogger().setLevel(numeric_level)
    logger.setLevel(numeric_level)


def init_env():
    args = parse_arg()

    setloglevel(config["loglevel"].get(), args)

    if args.operation != "create":
        # Load from project root directory. Assumption we are
        # operating from the project root
        config.set_file("config_default.yaml")

    metadata_query_fl = resources.path(
        "hmddops_resources.config", "metadata_query.yaml"
    )
    with resources.path("hmddops_resources.config", "metadata_query.yaml") as p:
        config.set_file(p.resolve())

    logger.debug("configs list ...")
    if args.config is not None:
        for c in args.config:
            logger.info(f" Adding config file : {c} ")
            config.set_file(c)

    db = os.environ.get("SNOWSQL_DATABASE")
    schema = os.environ.get("SNOWSQL_SCHEMA")
    logger.info(f"__OPER_DB_INFO__ : {db}.{schema}")

    return (args, config, db, schema)


def hmddops_create():
    # The current working directory will be considered as the
    # project root

    cwd = os.getcwd()

    print(" Creating artifacts directories ...")
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
        os.path.join(registry_dir, "verify"),
        os.path.join(registry_dir, "revert"),
        os.path.join(registry_dir, "deploy"),
    ]:
        os.makedirs(d, exist_ok=True)

    print(" Creating configuration file ...")
    fl_content = resources.read_text("hmddops_resources.config", "config.yaml")
    Path("config_default.yaml").write_text(fl_content)

    print(" Creating base script templates ...")
    with resources.path("hmddops_resources", "templates") as p:
        for c in p.iterdir():
            if c.is_file() == False:
                continue

            script_fl = Path(os.path.join(templates_dir, c.name))
            script_fl.write_text(c.read_text())


def hmddops_merge(p_db, p_schema):
    logger.info("\n\n __OPER__ : MERGE \n\n**********************************")
    merger = RegistryMerger(config)
    merger.do()


def hmddops_import(p_db, p_schema):
    logger.info("\n\n __OPER__ : IMPORT \n\n**********************************")

    session_tag = config["PLAN"]["session_tag"].get() + p_db + "_" + p_schema
    meta_fetcher = MetadataFetch(config, p_db, p_schema)
    meta_fetcher.open(session_tag)
    meta_fetcher.fetch_and_store_tolocal()

    # compare with registry
    doer = DeltaIdentifier(config)
    d_df = doer.do(p_db, p_schema)

    # get ddl for delta objects and store
    meta_fetcher.fetch_ddls_and_store_tolocal()

    generator = ScriptGenerator(config)
    generator.do()


def hmddops_plan(p_db, p_schema):
    logger.info("\n\n __OPER__ : PLAN \n\n**********************************")

    doer = PlanPhase(config)
    d_df = doer.do()


def hmddops_apply(p_db, p_schema, p_args):
    logger.info("\n\n __OPER__ : APPLY \n\n**********************************")

    # perform action
    doer = ApplyPhase(config, p_db, p_schema)
    if p_args.dryrun == True:
        doer.do(None, p_args.dryrun)
        return

    session_tag = config["APPLY"]["session_tag"].get() + p_db + "_" + p_schema
    meta_fetcher = MetadataFetch(config, p_db, p_schema)
    meta_fetcher.open(session_tag)
    # TODO Get the state of the target
    # meta_fetcher.fetch_and_store_tolocal()

    d_df = doer.do(meta_fetcher, p_args.dryrun)

    meta_fetcher.close()


def main():
    (args, config, db, schema) = init_env()

    if args.operation == "create":
        hmddops_create()
    elif args.operation == "import":
        hmddops_import(db, schema)
    elif args.operation == "plan":
        hmddops_plan(db, schema)
    elif args.operation == "apply":
        hmddops_apply(db, schema, args)
    elif args.operation == "merge":
        hmddops_merge(db, schema)

    logger.info("Finished !!!")
