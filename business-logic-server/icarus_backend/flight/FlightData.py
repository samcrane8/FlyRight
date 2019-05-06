from django.utils.dateparse import parse_datetime


class FlightData:

    def __init__(self, id, title, type, description,
                 starts_at, ends_at, coordinates, scheduling_rule=None):
        self.id = id
        self.title = title
        self.type = type
        self.description = description
        self.starts_at = starts_at
        self.ends_at = ends_at
        self.coordinates = coordinates
        self.scheduling_rule = scheduling_rule

    @staticmethod
    def from_json(json_object):
        title = json_object['title']
        _type = json_object['type']
        starts_at = parse_datetime(json_object['starts_at'])
        ends_at = parse_datetime(json_object['ends_at'])
        description = json_object['description']
        coordinates = json_object['area']['features'][0]['geometry']['coordinates']
        if coordinates[0] is not coordinates[-1]:
            coordinates += [coordinates[0]]
        if 'id' in json_object.keys():
            id = json_object['id']
        else:
            id = ''
        return FlightData(id, title, _type, description, starts_at, ends_at, coordinates)