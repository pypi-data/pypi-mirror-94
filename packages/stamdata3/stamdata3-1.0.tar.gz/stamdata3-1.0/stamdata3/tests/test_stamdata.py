import os
import unittest
from typing import List

from stamdata3.Organisation import Organisation
from stamdata3.stamdata3 import Stamdata3
from stamdata3.Resource import Resource


class StamdataTestCase(unittest.TestCase):
    def setUp(self) -> None:
        file = os.path.join(os.path.dirname(__file__), 'test_data', 'stamdata.xml')
        self.stamdata = Stamdata3(file)

    def testResources(self):
        resources = self.stamdata.resources()
        resources = list(resources)

        resource = resources[0]
        self.assertIsInstance(resources[0], Resource)
        self.assertEqual(53453, resource.resource_id)
        self.assertEqual('AK', resource.company_code)

    def testOrganisations(self):
        organisations = self.stamdata.organisations()
        organisations = list(organisations)

        organisation = organisations[0]
        self.assertIsInstance(organisation, Organisation)
        self.assertEqual('AK', organisation.company_code)


if __name__ == "__main__":
    unittest.main()
