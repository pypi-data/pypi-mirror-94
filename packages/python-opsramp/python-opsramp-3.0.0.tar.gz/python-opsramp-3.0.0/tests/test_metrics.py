#!/usr/bin/env python
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

import unittest
import requests_mock

import opsramp.binding


class Metrics(unittest.TestCase):
    def setUp(self):
        fake_url = 'mock://api.example.com'
        fake_token = 'unit-test-fake-token'
        self.ormp = opsramp.binding.Opsramp(fake_url, fake_token)

    def test_get_metrics(self):
        examples = (
            'tenants/client_1234/metrics/mysql.cluster.status/metricType',
            'search?tenant=client_1234&resource=abcdef&metric=mysql.cluster.status'
        )
        group = self.ormp.metrics()
        for target in examples:
            url = group.api.compute_url(target)
            expected_receive = 'fake unit test value ' + target
            with requests_mock.Mocker() as m:
                m.get(url, text=expected_receive, complete_qs=True)
                actual = group.get(target)
                assert m.call_count == 1
                assert actual == expected_receive
