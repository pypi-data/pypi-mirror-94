#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import logging
import os
from uuid import uuid4
from panza.jobs import new_job_workspace
from panza.cache import Cache
from panza.config import PanzaConfiguration, AdditionalDockerDaemonConfiguration
from quixote import Fetcher
from quixote.fetch.copy import copy
from quixote.inspection import Scope
from typing import Any, Dict, List

from dulcinea import metadata


def create_argument_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--context-file", type=str)
    info_parser_group = arg_parser.add_mutually_exclusive_group()
    info_parser_group.add_argument("-i", "--info-file", type=str)
    info_parser_group.add_argument("--auto-info", action='store_true')
    arg_parser.add_argument("-r", "--root-dir", type=str, default="/tmp")
    arg_parser.add_argument("--docker-bridge-ip", type=str, default="10.9.8.7/24")
    arg_parser.add_argument("--override-deliveries", type=str)
    arg_parser.add_argument("--integrate", action='store_true', help=argparse.SUPPRESS)
    arg_parser.add_argument("--keep-cache", action='store_true', help='Keep the cache on successful run')
    arg_parser.add_argument("--version", action='version', version='%(prog)s {}'.format(metadata.__version__))
    arg_parser.add_argument("moulinette_directory", type=str)
    return arg_parser


def configure_logging():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    dulcinea_logger = logging.getLogger("dulcinea")
    dulcinea_logger.addHandler(console_handler)
    dulcinea_logger.setLevel(logging.DEBUG)
    panza_logger = logging.getLogger("panza.jobs")
    panza_logger.addHandler(console_handler)
    panza_logger.setLevel(logging.DEBUG)
    return dulcinea_logger


def load_context_file(cmd_args) -> Dict[str, Any]:
    ctx = {}
    if cmd_args.context_file:
        with open(cmd_args.context_file, 'r') as context_file:
            ctx = json.load(context_file)
    return ctx


def make_panza_config(cmd_args) -> PanzaConfiguration:
    return PanzaConfiguration(
        root_directory=f"{cmd_args.root_dir}/panza",
        additional_docker_daemon=AdditionalDockerDaemonConfiguration(
            network_bridge_mask=cmd_args.docker_bridge_ip,
        )
    )


def load_info(cmd_args, arg_parser) -> List[Dict]:
    if cmd_args.info_file:
        with open(cmd_args.info_file, 'r') as info_file:
            return json.load(info_file)
    elif cmd_args.auto_info:
        if cmd_args.override_deliveries is None:
            arg_parser.error("cannot use '--auto-info' without '--override-deliveries'")
        return sorted(
            [{"group_id": entry} for entry in os.listdir(cmd_args.override_deliveries)
             if os.path.isdir(f"{cmd_args.override_deliveries}/{entry}")],
            key=lambda d: d["group_id"]
        )
    else:
        arg_parser.error("missing either '--info-file' or '--auto-info'")


def failed_req_pretty_output(scope, indent=0):
    for entry in scope.entries:
        if isinstance(entry, Scope):
            sub_entries = [e for e in failed_req_pretty_output(entry, indent + 2 * (not entry.hidden))]
            if sub_entries:
                if entry.hidden is False:
                    yield " " * indent + entry.name
                for sub_entry in sub_entries:
                    yield sub_entry
        else:
            assert isinstance(entry, dict)
            if "requirements" in entry:
                ok, req = entry["requirements"]
                if not ok:
                    yield " " * indent + "requirement failed: " + str(req)
            elif "assertion_failure" in entry:
                yield " " * indent + "assertion failed: " + entry["assertion_failure"]


def main():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()

    fetch_context = load_context_file(args)
    infos = load_info(args, arg_parser)
    panza_config = make_panza_config(args)
    override_deliveries = args.override_deliveries
    run_identifier = uuid4()
    cache_dir = f"{args.root_dir}/fetcher_cache-{run_identifier}"
    cache = Cache.create_at(cache_dir, max_entries=32, exist_ok=False)

    logger = configure_logging()
    logger.debug("Using cache_dir=%s", cache_dir)

    request_date = datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')
    results = []

    for info in infos:
        try:
            defaults = {
                "leader": "login_x",
                "request_date": request_date,
                "module_id": 1,
                "activity_id": 1,
            }
            if "group_id" not in info:
                print(f"Warning: missing mandatory field 'group_id' in {info}, skipping")
                continue
            for k, v in defaults.items():
                info.setdefault(k, v)
            environment_name = f"dulcinea-{info['module_id']}-{info['activity_id']}"
            job_name = f"{info['module_id']}-{info['activity_id']}-{info['group_id']}"
            with new_job_workspace(panza_config, args.moulinette_directory, job_name) as workspace:
                if override_deliveries is None:
                    inspector_result = workspace \
                        .build_job_environment(environment_name) \
                        .fetch_data(context={**info, **fetch_context}, cache=cache) \
                        .execute_job(context=info)
                else:
                    handle = workspace.build_job_environment(environment_name)
                    handle.blueprint.fetchers = [Fetcher(lambda: copy(override_deliveries))]
                    inspector_result = handle \
                        .fetch_data(context={**info, **fetch_context}, cache=cache) \
                        .execute_job(context=info)
                results.append((str(info['group_id']), inspector_result))
        except Exception as e:
            print(f"Cannot execute job for delivery {info['group_id']}: {str(e)}")
            results.append(
                (str(info['group_id']), {"error": f"Cannot execute job: {str(e)}"})
            )

    print("\nRESULTS\n")
    any_crash, any_mismatching_status = False, False
    for name, result in results:
        print(f"Results for group {name}")
        if "error" in result:
            print("Status: CRASH")
            print(result["error"])
            any_crash = True
        else:
            job_result = result["result"]
            failed_reqs = list(iter(failed_req_pretty_output(job_result)))
            if not failed_reqs:
                print("Status: OK, all tests passed")
                any_mismatching_status = any_mismatching_status or not name.startswith("OK")
            else:
                print("Status: KO")
                print("\n".join(failed_reqs))
                any_mismatching_status = any_mismatching_status or not name.startswith("KO")
        print()
    if args.integrate is True:
        if any_crash or any_mismatching_status:
            print("Some jobs resulted in an unexpected status, integration failed")
            return 1

    if not any_crash and not any_mismatching_status and not args.keep_cache:
        print(f"Deleting {cache}")
        cache.remove()

    return 0


if __name__ == '__main__':
    exit(main())
