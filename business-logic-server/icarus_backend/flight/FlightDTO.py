from .FlightData import FlightData
from .FlightModel import Flight
from users.models import IcarusUser as User
from icarus_backend.clearance.ClearanceModel import Clearance
from django.contrib.gis.geos import Polygon
from icarus_backend.utils import set_lat_range

# TODO what does DTO mean?
class FlightDTO:

    @staticmethod
    def data_to_db(mission_data: FlightData, user: User, clearance: Clearance):
        area = []
        for coordinate in mission_data.coordinates:
            area += [[coordinate[0], set_lat_range(coordinate[1])]]
        area = Polygon(area)
        return Flight(id=mission_data.id, title=mission_data.title, type=mission_data.type,
                      description=mission_data.description, starts_at=mission_data.starts_at,
                      ends_at=mission_data.ends_at, area=area, created_by=user,
                      clearance=clearance)

    @staticmethod
    def db_to_data(flight: Flight):
        flight_dict = flight.as_dict()
        return FlightData(id=flight.id, title=flight.title, type=flight.type, description=flight.description,
                          starts_at=flight.starts_at, ends_at=flight.ends_at,
                          coordinates=flight_dict['area']['features'][0]['geometry']['coordinates'])

