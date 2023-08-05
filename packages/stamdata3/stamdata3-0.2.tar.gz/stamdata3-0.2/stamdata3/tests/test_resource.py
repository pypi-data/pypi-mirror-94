import os
import unittest

from stamdata3.stamdata3 import Stamdata3


class ResourceTestCase(unittest.TestCase):
    def test_resource_id(self):
        stamdata = Stamdata3(os.path.join(os.path.dirname(__file__), 'test_data', 'stamdata.xml'))
        resource = stamdata.resource(53453)
        self.assertEqual(resource.resource_id, 53453)


if __name__ == '__main__':
    unittest.main()
