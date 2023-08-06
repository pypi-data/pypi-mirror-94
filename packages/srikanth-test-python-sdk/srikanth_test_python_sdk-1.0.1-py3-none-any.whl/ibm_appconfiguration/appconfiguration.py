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

from .feature.internal.utils.validators import Validators
from .feature.models import Feature, FeatureType
from .core.internal import Logger
from .feature.internal.common import constants
from typing import List, Optional
from .feature.feature_handler import FeatureHandler

try:
    import thread
except ImportError:
    import _thread as thread


class AppConfiguration:
    __instance = None

    # regions
    REGION_US_SOUTH = "us-south"
    REGION_EU_GB = "eu-gb"
    overrideServerHost = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AppConfiguration.__instance is None:
            return AppConfiguration()
        return AppConfiguration.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AppConfiguration.__instance is not None:
            raise Exception("AppConfiguration " + constants.SINGLETON_EXCEPTION)
        else:
            self.__apikey = ''
            self.__region = ''
            self.__featureHandlerInstance = None
            self.__guid = ''
            self.__isInitialized = False
            self.__is_initialized_feature = False
            AppConfiguration.__instance = self

    def init(self, region: str, guid: str, apikey: str):

        if not Validators.validateString(region):
            Logger.error(constants.REGION_ERROR)
            return
        if not Validators.validateString(apikey):
            Logger.error(constants.APIKEY_ERROR)
            return
        if not Validators.validateString(guid):
            Logger.error(constants.GUID_ERROR)
            return
        self.__apikey = apikey
        self.__region = region
        self.__guid = guid
        self.__isInitialized = True
        self.__setup_feature_handler()

    def get_region(self) -> str:
        return self.__region

    def get_guid(self) -> str:
        return self.__guid

    def get_apikey(self) -> str:
        return self.__apikey

    def __setup_feature_handler(self):
        self.__featureHandlerInstance = FeatureHandler.get_instance()
        self.__featureHandlerInstance.init(apikey=self.__apikey,
                                           guid=self.__guid,
                                           region=self.__region,
                                           override_server_host=self.overrideServerHost)
        self.__is_initialized_feature = True

    def fetch_features_from_file(self,
                                 feature_file: Optional[str] = None,
                                 live_feature_update_enabled: Optional[bool] = True):
        if not self.__isInitialized or not self.__is_initialized_feature:
            Logger.error(constants.COLLECTION_ID_ERROR)
            return

        if not live_feature_update_enabled and feature_file is None:
            Logger.error(constants.FEATURE_FILE_NOT_FOUND_ERROR)
            return
        self.__featureHandlerInstance.fetch_features_from_file(feature_file=feature_file,
                                                               live_feature_update_enabled=live_feature_update_enabled)
        thread.start_new_thread(self.__featureHandlerInstance.load_data, ())
        return

    def set_collection_id(self, collection_id: str):

        if not self.__isInitialized or not self.__is_initialized_feature:
            Logger.error(constants.COLLECTION_ID_ERROR)
            return

        if not Validators.validateString(collection_id):
            Logger.error(constants.COLLECTION_ID_VALUE_ERROR)
            return

        self.__featureHandlerInstance.set_collection_id(collection_id=collection_id)
        self.__is_initialized_feature = True
        thread.start_new_thread(self.__featureHandlerInstance.load_data, ())
        return

    def fetch_feature_data(self):
        if self.__isInitialized and self.__is_initialized_feature:
            thread.start_new_thread(self.__featureHandlerInstance.load_data, ())
        else:
            Logger.error(constants.COLLECTION_SUB_ERROR)

    def register_features_update_listener(self, listener):
        if self.__isInitialized and self.__is_initialized_feature:
            self.__featureHandlerInstance.register_features_update_listener(listener)
        else:
            Logger.error(constants.COLLECTION_SUB_ERROR)

    def get_feature(self, feature_id: str) -> Feature:
        if self.__isInitialized and self.__is_initialized_feature:
            return self.__featureHandlerInstance.get_feature(feature_id)
        else:
            Logger.error(constants.COLLECTION_SUB_ERROR)
            return None

    def get_features(self) -> List[Feature]:
        if self.__isInitialized and self.__is_initialized_feature:
            return self.__featureHandlerInstance.get_features()
        else:
            Logger.error(constants.COLLECTION_SUB_ERROR)
            return None

    def enable_debug(self, enable: bool):
        Logger.set_debug(enable)
