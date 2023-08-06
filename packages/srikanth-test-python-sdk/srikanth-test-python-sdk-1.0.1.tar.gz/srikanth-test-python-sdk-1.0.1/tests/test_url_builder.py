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


import unittest
from ibm_appconfiguration.feature.internal.utils.url_builder import URLBuilder
from ibm_appconfiguration.appconfiguration import AppConfiguration


class MyTestCase(unittest.TestCase):

    def test_url_builder(self):

        appcnf = AppConfiguration.get_instance()
        app_guid = '111-111-22003-5555-33'
        apikey = 'vc-hfggye0-rb4-kshfu5-3hht-5'
        appcnf.init(AppConfiguration.REGION_US_SOUTH, app_guid, apikey)
        collection_id = 'collection_id_value'
        URLBuilder.init_with_collection_id(collection_id,'us-south',app_guid,'')

        config_url = URLBuilder.get_config_url()
        self.assertIsNotNone(config_url)
        l = URLBuilder.get_web_socket_url()
        l1 = URLBuilder.get_web_socket_url()
        self.assertEqual(l, l1)
        self.assertIsNotNone(URLBuilder.get_web_socket_url())
        self.assertIsNotNone(URLBuilder.get_metering_url())


        expected_config_url = 'https://us-south.apprapp.cloud.ibm.com/apprapp/feature/v1/instances/{0}/collections/{1}/config'.format(app_guid, collection_id)
        self.assertEqual(config_url, expected_config_url)

        cutom_route = 'https://apprapp-tester-clusterh53t283.testing.containers.appdomain.cloud'
        AppConfiguration.overrideServerHost = cutom_route
        URLBuilder.init_with_collection_id(collection_id,'us-south',app_guid,cutom_route)
        expected_config_url = '{0}/apprapp/feature/v1/instances/{1}/collections/{2}/config'.format(cutom_route, app_guid, collection_id)
        config_url = URLBuilder.get_config_url()
        self.assertEqual(config_url, expected_config_url)


if __name__ == '__main__':
    unittest.main()
