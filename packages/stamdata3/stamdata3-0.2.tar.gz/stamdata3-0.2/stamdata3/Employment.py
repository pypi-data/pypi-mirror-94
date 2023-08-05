from stamdata3.Relation import Relation
from stamdata3.XMLDataHelper import XMLDataHelper
from stamdata3.exceptions import InvalidRelation


class Employment(XMLDataHelper):
    @property
    def resource_id(self):
        return self.data.get('ResourceId')

    @property
    def type(self):
        return self.string('EmploymentType')

    @property
    def type_description(self):
        return self.string('EmploymentTypeDescription')

    @property
    def percentage(self):
        return self.float('Percentage')

    @property
    def post_id(self):
        return self.string('PostId')

    @property
    def post_id_description(self):
        return self.string('PostIdDescription')

    @property
    def post_code(self):
        return self.string('PostCode')

    @property
    def post_code_description(self):
        return self.string('PostCodeDescription')

    @property
    def date_from(self):
        return self.date('DateFrom')

    @property
    def date_to(self):
        return self.date('DateTo')

    @property
    def last_update(self):
        return self.date_time('LastUpdate')

    @property
    def sequence_ref(self):
        return self.int('SequenceRef')

    @property
    def main_position(self):
        return self.bool('MainPosition')

    def relation(self, relation_type):
        relation = self.data.find(
            'Relations/Relation[@ElementType="%s"]' % relation_type)
        if relation is None:
            raise InvalidRelation(
                'Employment %s has no relation of type %s' % (self.data.get('ResourceId'), relation_type))
        else:
            return Relation(relation)

    def __str__(self):
        return '%s %s' % (self.resource_id, self.post_code_description)

