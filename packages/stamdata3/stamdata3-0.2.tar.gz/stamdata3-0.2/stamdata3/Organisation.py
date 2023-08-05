from stamdata3.XMLDataHelper import XMLDataHelper


class Organisation(XMLDataHelper):
    @property
    def company_code(self):
        return self.string('CompanyCode')

    @property
    def name(self):
        return self.string('Name')

    @property
    def id(self):
        return self.string('Id')

    @property
    def parent_id(self):
        return self.string('ParentId')

    @property
    def manager(self):
        return self.int('Managers/string')

    @property
    def status(self):
        return self.string('Status')
