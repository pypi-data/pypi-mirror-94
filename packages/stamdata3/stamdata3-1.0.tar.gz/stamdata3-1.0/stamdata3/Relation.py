from stamdata3.XMLDataHelper import XMLDataHelper


class Relation(XMLDataHelper):
    @property
    def value(self):
        return self.string('Value')

    @property
    def description(self):
        return self.string('Description')

    @property
    def date_from(self):
        return self.date('DateFrom')

    @property
    def date_to(self):
        return self.date('DateFrom')

    def __str__(self):
        return '%s %s' % (self.value, self.description)
