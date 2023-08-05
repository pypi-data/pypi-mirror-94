from datetime import datetime

from stamdata3.Employment import Employment


def map_employment(employment):
    return Employment(employment)


class Resource:
    def __init__(self, employee):
        self.employee = employee

    @property
    def resource_id(self):
        return int(self.employee.find('ResourceId').text)

    @property
    def address(self):
        return self.employee.find('Addresses/Address')

    @property
    def employments(self):
        employments = self.employee.findall('Employments/Employment')
        return map(map_employment, employments)

    def main_position(self):
        employment = self.employee.find(
            'Employments/Employment/MainPosition[.="true"]/..')
        if not employment:
            raise AttributeError('Employee %s has no MainPosition' %
                                 self.resource_id)
        else:
            return Employment(employment)

    @property
    def first_name(self):
        return self.employee.find('FirstName').text

    @property
    def last_name(self):
        return self.employee.find('Surname').text

    @property
    def company_code(self):
        return self.employee.find('CompanyCode').text

    @property
    def birth_date(self):
        date = self.employee.find('Birthdate').text
        return datetime.strptime(date, '%Y-%m-%d')

    @property
    def ssn(self):
        return self.employee.find('SocialSecurityNumber').text

    @property
    def status(self):
        return self.employee.find('Status').text
