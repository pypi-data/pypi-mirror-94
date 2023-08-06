# (C) Copyright IBM Corp. 2021.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.


from __future__ import absolute_import

import unittest
from ibm_appconfiguration.feature.models import Segment


class MyTestCase(unittest.TestCase):
    sut = None

    def set_up(self):
        segment = {
            'name': 'RegionalUser',
            'segment_id': 'kdu77n4s',
            'rules': [
                {
                    'values': [
                        100
                    ],
                    'operator': 'lesserThanEquals',
                    'attribute_name': 'radius'
                },
                {
                    'values': [
                        50
                    ],
                    'operator': 'lesserThan',
                    'attribute_name': 'cityRadius'
                }
            ]
        }

        self.sut = Segment(segment)

    def test_segment(self):
        self.set_up()
        client_attributes = {
            'radius':  100,
            'cityRadius': 35
        }
        self.assertTrue(self.sut.evaluateRule(client_attributes))


if __name__ == '__main__':
    unittest.main()
