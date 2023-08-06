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
from app_configuration.feature.internal.utils.validators import Validators


class MyTestCase(unittest.TestCase):
    def test_validator(self):

        str_val = ""
        self.assertEqual(Validators.validateString(str_val), False)
        str_val = "hello"
        self.assertEqual(Validators.validateString(str_val), True)

    def test_generic(self):

        value = 3
        expected = Validators.convertValue(value, int)
        self.assertEqual(expected, 3)

        value = "False"
        expected = Validators.convertValue(value, str)
        self.assertEqual(expected, value)

        value = "String"
        expected = Validators.convertValue(value, str)
        self.assertEqual(expected, value)

        value = 1.0
        expected = Validators.convertValue(value, float)
        self.assertEqual(expected, value)

        value = 10.4539943
        expected = Validators.convertValue(value, float)
        self.assertEqual(expected, value)

        value = False
        expected = Validators.convertValue(value, bool)
        self.assertEqual(expected, value)

        value = True
        expected = Validators.convertValue(value, bool)
        self.assertEqual(expected, value)



if __name__ == '__main__':
    unittest.main()
