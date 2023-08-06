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

class Rule:
    """
          Attributes:
           rules (dict): rules JSON object that contains all the Rules.
      """

    def __init__(self, rules=dict()):
        self.__attribute_name = rules.get("attribute_name", "")
        self.__operator = rules.get("operator", "")
        self.__values = rules.get("values", list())

    def get_attributes(self) -> str:
        return self.__attribute_name

    def get_operator(self) -> str:
        return self.__operator

    def get_values(self) -> list:
        return self.__values

    def __endsWith(self, key: str, value: str) -> bool:
        return key.endswith(value)

    def __startsWith(self, key: str, value: str) -> bool:
        return key.startswith(value)

    def __contains(self, key: str, value: str) -> bool:
        return key in value

    def __is(self, key: str, value: str) -> bool:
        if type(key) is type(value):
            return key == value
        else:
            return False

    def __greaterThan(self, key: str, value: str) -> bool:
        if type(key) is type(value) and str(key).isnumeric():
            return key > value
        else:
            return False

    def __lesserThan(self, key: str, value: str) -> bool:
        if type(key) is type(value) and str(key).isnumeric():
            return key < value
        else:
            return False

    def __greaterThanEquals(self, key: str, value: str) -> bool:
        if type(key) is type(value) and str(key).isnumeric():
            return key >= value
        else:
            return False

    def __lesserThanEquals(self, key: str, value: str) -> bool:
        if type(key) is type(value) and str(key).isnumeric():
            return key <= value
        else:
            return False

    def __operatorCheck(self, keyData=None, valueData=None) -> bool:
        key = keyData
        value = valueData

        result = False

        if key is None or value is None:
            return result

        case_checker = {
            "endsWith": lambda key, value: self.__endsWith(key, value),
            "startsWith": lambda key, value: self.__startsWith(key, value),
            "contains": lambda key, value: self.__contains(key, value),
            "is": lambda key, value: self.__is(key, value),
            "greaterThan": lambda key, value: self.__greaterThan(key, value),
            "lesserThan": lambda key, value: self.__lesserThan(key, value),
            "greaterThanEquals": lambda key, value: self.__greaterThanEquals(key, value),
            "lesserThanEquals": lambda key, value: self.__lesserThanEquals(key, value)
        }

        return case_checker.get(self.__operator, False)(key, value)

    def evaluateRule(self, client_attributes: dict, query_map: dict, header_map: dict, body_map: dict) -> bool:

        result = False
        lower_case_attr = self.__attribute_name.lower()

        if self.__attribute_name in client_attributes:
            key = client_attributes.get(self.__attribute_name)
        elif lower_case_attr in header_map:
            key = header_map.get(lower_case_attr)
        elif self.__attribute_name in body_map:
            key = body_map.get(self.__attribute_name)
        elif self.__attribute_name in query_map:
            key = query_map.get(self.__attribute_name)
        else:
            return result
        for i in range(0, len(self.__values)):
            value = self.__values[i]
            if self.__operatorCheck(key, value):
                result = True

        return result
