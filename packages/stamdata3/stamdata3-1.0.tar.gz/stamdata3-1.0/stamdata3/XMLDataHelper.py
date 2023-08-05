from datetime import datetime

from stamdata3.exceptions import InvalidField


class XMLDataHelper:
    def __init__(self, data):
        if data is None:
            raise ValueError('Data is None')
        self.data = data

    def get_field(self, field):
        data = self.data.find(field)
        if data is None:
            raise InvalidField('Field %s does not exist' % field)
        elif data.text is None:
            return None
        else:
            return data.text

    def string(self, field):
        data = self.get_field(field)
        if data is None:
            return None
        else:
            return data

    def bool(self, field):
        data = self.string(field)
        if data == 'false':
            return False
        elif data == 'true':
            return True
        else:
            raise ValueError('Invalid boolean value: %s' % data)

    def int(self, field):
        return int(self.get_field(field))

    def float(self, field):
        return float(self.get_field(field))

    def date(self, field):
        data = self.string(field)
        return datetime.strptime(data, '%Y-%m-%d').date()

    def date_time(self, field):
        data = self.string(field)
        return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
