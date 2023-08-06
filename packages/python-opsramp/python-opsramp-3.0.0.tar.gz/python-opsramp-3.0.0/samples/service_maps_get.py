#!/usr/bin/env python
#
# Exercise the opsramp module as an illustration of how to use it.
#
# (c) Copyright 2020-2021 Hewlett Packard Enterprise Development LP
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
import logging
import argparse

import opsramp.binding


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


def walk(service_maps, map):
    if map['childType'] != 'SERVICE':
        # print("LEAF! %s %s" % (map['id'], map['name']))
        print("LEAF! %s" % map)
    else:
        # print("BRANCH! %s %s" % (map['id'], map['name']))
        print("BRANCH! %s" % map)
        maps = service_maps.get(map['id'])
        if 'results' in maps:
            for submap in maps['results']:
                walk(service_maps, submap)


def main():
    ns = parse_argv()
    if ns.debug:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

    tnt_id = os.environ['OPSRAMP_TENANT_ID']

    ormp = connect()
    tnt = ormp.tenant(tnt_id)

    service_maps = tnt.service_maps()
    resp = service_maps.get()
    for map in resp['results']:
        walk(service_maps, map)


if __name__ == "__main__":
    main()
