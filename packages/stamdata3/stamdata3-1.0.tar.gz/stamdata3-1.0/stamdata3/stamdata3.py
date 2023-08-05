from xml.etree import ElementTree

from stamdata3.Organisation import Organisation
from stamdata3.Resource import Resource


class Stamdata3:
    root = None

    def __init__(self, file):
        tree = ElementTree.parse(file)
        self.root = tree.getroot()

    def resource(self, resource_id):
        resource = self.root.find(
            './/Resources/Resource/ResourceId[.="%d"]/..' % resource_id)
        if not resource:
            raise ResourceNotFound
        return Resource(resource)

    def resources(self):
        """
        Get all resources

        :rtype: Iterable[Resource]
        """
        resources = self.root.findall('Resources/Resource')
        return map(map_resource, resources)

    def organisations(self):
        """
        Get all organisations

        :rtype: Iterable[Organisation]
        """
        organisations = self.root.findall('Organisations/Organisation')
        return map(map_organisation, organisations)


def map_resource(resource):
    return Resource(resource)


def map_organisation(organisation):
    return Organisation(organisation)


class ResourceNotFound(Exception):
    pass

# stamdata = Stamdata3()
# print(stamdata.employee_address(53898))
