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
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from ibm_appconfiguration import AppConfiguration, Feature, FeatureType
import config
import time
import secrets

has_data = True


def response():
    print('Get your Feature value NOW')


def setup() -> None:
    app_config = AppConfiguration.get_instance()
    app_config.init(region=AppConfiguration.REGION_US_SOUTH,
                    guid=config.GUID,
                    apikey=config.APIKEY)
    app_config.set_collection_id(config.COLLECTION)
    app_config.fetch_features_from_file(live_feature_update_enabled=True, feature_file=config.FILE)

def fetch_feature(feature_id: str, request_object=None) -> str:
    if has_data:
        app_config = AppConfiguration.get_instance()
        feature = app_config.get_feature(feature_id)
        try:
            if feature:
                identity = {
                    'city': 'Bangalore',
                    'country': 'India'
                }
                if feature.get_feature_data_type() == FeatureType.STRING:
                    val = feature.get_current_value(id='pvQr45', identity_attributes=identity)
                    return f"Your feature value is {val}"
                elif feature.get_feature_data_type() == FeatureType.BOOLEAN:
                    val = feature.get_current_value('pvQr45', identity)
                    return f"Your feature value is {val}"
                elif feature.get_feature_data_type() == FeatureType.NUMERIC:
                    val = feature.get_current_value('pvQr45', identity)
                    return f"Your feature value is {val}"
            else:
                return "Not loaded"
        except Exception as err:
            print(err)
            return "Not loaded"

    else:
        return "Not loaded"


def _html(message):
    """This just generates an HTML document that includes `message`
    in the body. Override, or re-write this do do more interesting stuff.
    """
    content = f"<html><body><h1>{message}</h1></body></html>"
    return content.encode("utf8")  # NOTE: must return a bytes object!


class MockServer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        emails = ['tester@google.com', 'premium@ibm.com']
        app_config = AppConfiguration.get_instance()
        email = secrets.choice(emails)

        feature = app_config.get_feature("featurestring")

        identity = {
            'id': 'pvqr',
            "email": email
        }
        value = feature.get_current_value("pvQr45", identity)

        is_valid = True
        if value == "Hello Googler":
            is_valid = "tester@google.com" == email
        elif value == "Hello IBMer":
            is_valid = "premium@ibm.com" == email

        self.wfile.write(json.dumps({'is_valid': is_valid, 'featurevalue': value,
                                     'time': round(time.time() * 1000)}).encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        value = "POST!"
        if has_data:
            value = fetch_feature("featurestring", self)
        self._set_headers()
        self.wfile.write(_html(value))


def run(server_class=HTTPServer, handler_class=MockServer, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    setup()
    run()
