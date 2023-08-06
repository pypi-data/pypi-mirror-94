#!/usr/bin/env python3

'''Veris worker for the ACT platform

Copyright 2019 the ACT project <opensource@mnemonic.no>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
'''

import argparse
import csv
import io
import json
import os
import re
import sys
import traceback
import zipfile
from logging import error, warning
from typing import Any, Dict, Optional, Text, Union, cast

import requests

import act.api
from act.api.helpers import handle_fact
from act.workers.libs import urlcache, worker

VERSION = "0.1"
ISO_3166_FILE = "https://raw.githubusercontent.com/lukes/" + \
    "ISO-3166-Countries-with-Regional-Codes/master/all/all.json"


def get_cn_map(filename: Text) -> Dict:
    """
    Read file with county information (ISO 3166 from filename)
    return map with country code (e.g. "NO") as key, and Country
    Name (e.g. "Norway" as value)
    """
    cn_map = {}

    for c_map in json.loads(open(filename, "r", encoding="utf8").read()):
        cn_map[c_map["alpha-2"]] = c_map["name"]

    return cn_map


def parseargs() -> argparse.ArgumentParser:
    """ Parse arguments """
    parser = worker.parseargs('Shadowserver ASN enrichment')
    parser.add_argument(
        '--country-codes',
        help="Should point to file downloaded from {}".format(ISO_3166_FILE))
    parser.add_argument('--veris-campaign', help='Read mapping of veris campaign from (CSV) file')
    parser.add_argument('--threat-actor-variety', help='Varieties to use as Threat Actors', default="Activist, Organized crime, Nation-state")
    parser.add_argument('--hash-url-matching', help='Download and hash references matching regular expression', default=r'^(.*pdf)$')
    parser.add_argument('--veris-prefix', help='Prefix for incidents and campaign IDs. E.g use "VCDB" for Veris Community Database"')
    parser.add_argument('--veris-url', help='Read veris incidents from URL.')
    parser.add_argument('--veris-file', help='Read veris incidents from File.')
    parser.add_argument('--stdin', action='store_true', help='Read veris incidents on stdin.')
    return parser


def handle_reports(config: Dict[Text, Any], incident: Dict[Text, Any], incident_id: Text) -> None:
    """
    Extract all references in incident. For each (URL-)reference, check whether we should
    download the content and creaa a sha256 hash digest of it (must match config["hash_url_matching"]).
    The sha256 hash is also cached locally.
    """

    # Split references by ";"
    references = [ref.strip() for ref in incident.get("reference", "").split(";") if ref.strip()]

    if references:
        for ref in references:
            if not re.search(config["hash_url_matching"], ref):
                continue

            report_hash = config["db_cache"].query_download_update(ref)

            if report_hash:
                handle_fact(
                    config["actapi"].fact("mentions")
                    .source("report", report_hash)
                    .destination("incident", incident_id),
                    output_format=config["output_format"]
                )


def handle_organizations(config: Dict[Text, Any], incident: Dict[Text, Any], incident_id: Text) -> None:
    """
    Create facts:
        * incident -targets-> organization
        * organization -locatedIn-> country
    """
    victim = incident.get("victim", {}).get("victim_id")

    if not victim:
        return

    handle_fact(
        config["actapi"].fact("targets")
        .source("incident", incident_id)
        .destination("organization", victim),
        output_format=config["output_format"]
    )

    for country_code in incident.get("victim", {}).get("country", []):
        country = config["cn_map"].get(country_code)

        if country:
            handle_fact(
                config["actapi"].fact("locatedIn")
                .source("organization", victim)
                .destination("country", country),
                output_format=config["output_format"]
            )


def handle_threat_actor(config: Dict[Text, Any], incident: Dict[Text, Any], incident_id: Text) -> None:
    """
    Creat facts from actor->external, where the variety includes at least on variety specified in config["threat_actor_variety"]

    """

    external_actor = incident.get("actor", {}).get("external", {})

    if not external_actor:
        return  # No threat actors

    # Varieties are "tags" on actors and we do not want to include all type of actors
    # Make sure at least one of the varieties are in the list of the configured varieties to include
    if any([variety in config["threat_actor_variety"] for variety in external_actor.get("variety", [])]):
        threat_actors = [ta.strip() for ta in incident.get("actor", {}).get("external", {}).get("name", [])]

        for ta in threat_actors:
            handle_fact(
                config["actapi"].fact("attributedTo")
                .source("incident", incident_id)
                .destination("threatActor", ta),
                output_format=config["output_format"]
            )


def handle_tool(config: Dict[Text, Any], incident: Dict[Text, Any], incident_id: Text) -> None:
    "Create content -classifiedAs-> tool, and fact chain from content to incident. "

    # Both "," and ";" are used to separate tools :(

    tools = [
        malware.strip().lower()
        for malware in re.split(r';|,', incident.get("action", {}).get("malware", {}).get("name", ""))
        if malware]

    for tool in tools:
        chain = act.api.fact.fact_chain(
            config["actapi"].fact("classifiedAs")
            .source("content", "*")
            .destination("tool", tool),
            config["actapi"].fact("observedIn")
            .source("content", "*")
            .destination("event", "*"),
            config["actapi"].fact("attributedTo")
            .source("event", "*")
            .destination("incident", incident_id),
        )

        for fact in chain:
            handle_fact(fact, output_format=config["output_format"])


def handle_campaign(config: Dict[Text, Any], incident: Dict[Text, Any], incident_id: Text) -> None:
    """
    Create incident -attributedTo-> campaign facts
    If we have a mapping from campaign (UUID) to name, a campaign -name-> will also be created
    """

    campaign = "{}-{}".format(
        config["veris_prefix"],
        incident["campaign_id"]) if incident.get("campaign_id") else None

    if not campaign:
        return

    handle_fact(
        config["actapi"].fact("attributedTo")
        .source("incident", incident_id)
        .destination("campaign", campaign),
        output_format=config["output_format"]
    )

    name = config["campaign_map"].get(format(campaign))

    if name:
        handle_fact(
            config["actapi"].fact("name", name)
            .source("campaign", campaign),
            output_format=config["output_format"]
        )

    else:
        warning("No name found for campaign {}. Make sure veris-campaign is provided and the ID is included in csv field (without prefix)".format(campaign))


def handle_incident(config: Dict[Text, Any], incident: Dict[Text, Any]) -> None:
    """ handle veris incidents
    """

    incident_id = "{}-{}".format(config["veris_prefix"], incident["incident_id"])

    handle_reports(config, incident, incident_id)
    handle_organizations(config, incident, incident_id)
    handle_tool(config, incident, incident_id)
    handle_threat_actor(config, incident, incident_id)
    handle_campaign(config, incident, incident_id)


def handle_zip_file(config: Dict[Text, Any], zfile: Union[Text, io.BytesIO]) -> None:
    "Read incident form all (json) files in zip file"

    # ZipFile accepts both file names (str) and file like objects
    zf = zipfile.ZipFile(zfile, "r")

    for fileinfo in zf.infolist():
        for incident in json.loads(zf.read(fileinfo).decode('utf-8')):
            handle_incident(config, incident)


def process(config: Dict[Text, Any]) -> None:
    "Process inicdent from stdin, url or file. URL and File supports zipped files in zip-format."

    # Read incident from stdin
    if config["stdin"]:
        for incident in sys.stdin.read().split("\n"):
            handle_incident(config, json.loads(incident))

        return

    # Download incidents from URL
    if config["veris_url"]:
        req = requests.get(config["veris_url"], proxies=config["proxies"], timeout=config["http_timeout"])
        if config["veris_url"].endswith(".zip"):
            handle_zip_file(config, io.BytesIO(req.content))
        else:
            for incident in req.json():
                handle_incident(config, cast(Dict, incident))
        return

    # Read incidents from file
    if config["veris_file"]:
        if config["veris_file"].endswith(".zip"):
            handle_zip_file(config, config["veris_file"])
        else:
            with open(config["veris_file"]) as f:
                for incident in json.loads(f.read()):
                    handle_incident(config, cast(Dict, incident))
        return

    error("Must specifiy either --stdin, --veris-url or --veris-file")


def get_campaigns(veris_prefix: Text, filename: Text) -> Optional[Dict[Text, Text]]:
    """
    Get mapping from campaign (UUID) to name
    """
    with open(filename) as csvfile:
        return {"{}-{}".format(veris_prefix, row[0]): row[1] for row in csv.reader(csvfile, delimiter=',')}


def main() -> None:
    """main function"""

    # Look for default ini file in "/etc/actworkers.ini" and ~/config/actworkers/actworkers.ini
    # (or replace .config with $XDG_CONFIG_DIR if set)
    args = worker.handle_args(parseargs())
    actapi = worker.init_act(args)

    if not args.country_codes:
        worker.fatal("You must specify --country-codes on command line or in config file")

    if not args.veris_prefix:
        worker.fatal("You must specify --veris-prefix")

    if not (args.veris_url or args.veris_file or args.stdin):
        worker.fatal("You must specify --veris-url, --veris-file or --stdin")

    args.veris_prefix = args.veris_prefix.upper()

    if not os.path.isfile(args.country_codes):
        worker.fatal("Country/region file not found at specified location: {}".format(args.country_codes), 2)

    args.threat_actor_variety = [variety.strip() for variety in args.threat_actor_variety.split(",")]

    # Configuration object that will be passed around to functions
    config = {
        # act API
        "actapi": actapi,

        # Map of CC -> Country Name
        "cn_map": get_cn_map(args.country_codes),

        # Map of CC -> Country Name
        "campaign_map": get_campaigns(args.veris_prefix, args.veris_campaign) if args.veris_campaign else {},

        # Cache of url > sha256
        "db_cache": urlcache.URLCache(
            requests_common_kwargs={
                "proxies": {
                    'http': args.proxy_string,
                    'https': args.proxy_string
                },
                "timeout": args.http_timeout
            }),

        "proxies": {
            'http': args.proxy_string,
            'https': args.proxy_string
        } if args.proxy_string else None,

    }

    # Add all arguments from args to config
    config.update(vars(args))

    process(config)


def main_log_error() -> None:
    "Main function. Log all exceptions to error"
    try:
        main()
    except Exception:
        error("Unhandled exception: {}".format(traceback.format_exc()))
        raise


if __name__ == '__main__':
    main_log_error()
