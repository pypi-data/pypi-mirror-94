import os
import unittest

from stamdata3.Employment import Employment
from stamdata3.exceptions import InvalidRelation
from stamdata3.stamdata3 import Stamdata3


class TestEmployment(unittest.TestCase):
    def setUp(self) -> None:
        self.stamdata = Stamdata3(os.path.join(os.path.dirname(__file__), 'test_data', 'stamdata.xml'))
        resource = self.stamdata.resource(53453)
        employments = list(resource.employments)
        self.employment: Employment = employments[0]

    def test_resource_id(self):
        self.assertEqual(self.employment.resource_id, '53453')

    def test_relation(self):
        stamdata = Stamdata3(os.path.join(os.path.dirname(__file__), 'test_data', 'stamdata_multi.xml'))
        resource = stamdata.resource(53453)
        employments = list(resource.employments)
        employment: Employment = employments[0]
        self.assertEqual(employment.relation('COST_CENTER').value, '1170')

    def test_invalid_relation(self):
        stamdata = Stamdata3(os.path.join(os.path.dirname(__file__), 'test_data', 'stamdata_multi.xml'))
        resource = stamdata.resource(53453)
        employments = list(resource.employments)
        employment: Employment = employments[0]
        with self.assertRaises(InvalidRelation):
            employment.relation('COST_CENTER_BAD').value


if __name__ == '__main__':
    unittest.main()
