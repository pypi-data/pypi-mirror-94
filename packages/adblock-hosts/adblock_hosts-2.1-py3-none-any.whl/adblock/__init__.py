#!/usr/bin/env python3
import logging
import os
import re
from logging.handlers import SysLogHandler

import yaml
from requests_futures.sessions import FuturesSession

DEFAULT_CONFIG = "/etc/adblock.conf"
DEFAULT_HOSTS_FILE = "/etc/adblock-hosts"
REPLACE_TARGET = "0.0.0.0"
REPLACE_TARGET_V6 = "::"

logger = logging.getLogger("adblock")
logger.setLevel(logging.DEBUG)

if not os.getuid():
    logger.addHandler(SysLogHandler())

session = FuturesSession(max_workers=16)


def load_config(configfile):
    with open(configfile) as f:
        return yaml.load(f.read(), Loader=yaml.SafeLoader)


def validate_config(loaded_config, hosts_file):
    try:
        with open(hosts_file, "w") as f:
            pass
    except PermissionError:
        logger.critical("Destination hosts file not writable! Exiting.")
        raise SystemExit
    if not loaded_config.get('sources'):
        logger.critical("No sources defined in /etc/adblock.conf or adblock.conf. Exiting.")
        raise SystemExit


def build_futures(sources):
    for source in sources:
        yield session.get(source)


def manipulate_results(config, key, results, discard=False):
    for item in config.get(key, []):
        if discard:
            results.discard(item)
        else:
            results.add(item)
    return results


def handle_blacklist(config, results):
    return manipulate_results(config, "blacklist", results)


def handle_whitelist(config, results):
    return manipulate_results(config, "whitelist", results, True)


def handle_whitelist_regex(config, results):
    whitelist = config.get("whitelist_regex")
    if whitelist:
        for host in list(results):
            for regex in whitelist:
                if re.match(regex, host):
                    results.discard(host)
                    break
    return results


def main():
    config = load_config(DEFAULT_CONFIG if os.access(DEFAULT_CONFIG, os.R_OK) else "adblock.conf")

    hosts_file = config.get("hosts_file", DEFAULT_HOSTS_FILE)
    replace_target = config.get("replace_target", REPLACE_TARGET)
    replace_target_v6 = config.get("replace_target_v6", REPLACE_TARGET_V6)

    validate_config(config, hosts_file)

    results = set()
    for future in build_futures(config["sources"]):
        response = future.result()
        if response.status_code == 200:
            logger.debug("Successfully retrieved %s", response.url)
            for line in response.text.split('\n'):
                if line and not line.startswith("#"):
                    try:
                        results.add(line.split()[1])
                    except IndexError:
                        pass
        else:
            logger.warning("Failed to retrieve %s: %d", response.url, response.status_code)

    handle_blacklist(config, results)
    handle_whitelist(config, results)
    handle_whitelist_regex(config, results)

    with open(hosts_file, 'w') as f:
        for host in results:
            f.write(''.join((replace_target, " ", host, '\n', replace_target_v6, " ", host, "\n")))


if __name__ == "__main__":
    main()