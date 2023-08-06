#!/usr/bin/env python
#
# Exercise the opsramp module as an illustration of how to use it.
#
# (c) Copyright 2019-2021 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json
import logging
import argparse

import opsramp.binding

# Example input JSON file with the bare minimum mandatory fields:
# {
#   "name": "Todd Unctuous",
#   "address": "Craggy Island",
#   "country": "Ireland",
#   "timeZone": "Europe/London"
# }


def connect():
    url = os.environ['OPSRAMP_URL']
    key = os.environ['OPSRAMP_KEY']
    secret = os.environ['OPSRAMP_SECRET']
    return opsramp.binding.connect(url, key, secret)


def parse_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        action='store_true'
    )
    ns = parser.parse_args()
    return ns


def main():
    ns = parse_argv()
    if ns.debug:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

    partner_id = os.environ['OPSRAMP_TENANT_ID']

    jdata = json.load(sys.stdin)
    print(jdata)

    ormp = connect()
    partner = ormp.tenant(partner_id)
    if partner.is_client():
        print(partner_id, 'is not a partner-level tenant')
        exit(2)

    group = partner.clients()
    resp = group.create(jdata)
    print(resp)


if __name__ == "__main__":
    main()
