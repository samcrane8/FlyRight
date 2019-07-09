import datetime
import numpy as np
from icarus_backend.flight.FlightModel import Flight
from users.models import IcarusUser as User
from icarus_backend.department.DepartmentModel import Department
from icarus_backend.department.tasks import DepartmentTasks
from django.utils import timezone
from django.contrib.gis.geos import Polygon
from django.db.models import Q


class DepartmentController:

    @staticmethod
    def create(name, owner_id, area, airbosses=[], watch_commanders=[]) -> (int, dict):
        numpy_area = np.asarray(area)
        if not (len(numpy_area.shape) == 3 and numpy_area.shape[2] == 2):
            return 400, {'message': 'Area is not properly formatted. Must have shape (-1, -1, 2).'}
        area = [[x[1],x[0]] for x in area[0]]
        area = Polygon(area)
        department = Department.objects.filter(name=name).first()
        if department:
            return 400, {'message': 'Department name already taken.'}
        owner = User.objects.filter(id=owner_id).first()
        department = Department(name=name, area=area, owner=owner)
        for airboss in airbosses:
            department.airbosses.add(airboss)
        for watch_commander in watch_commanders:
            department.watchCommanders.add(watch_commander)
        department.save()
        return 200, {'message': 'Department created.'}

    @staticmethod
    def edit(name, new_name, area) -> (int, dict):
        area = Polygon(area)
        department = Department.objects.filter(name=name).first()
        if not department:
            return 400, {'message': 'No department with this name exists.'}
        department.area = area
        department.name = new_name
        department.save()
        return 200, {'message': 'Department edited.'}

    @staticmethod
    def get(area=None) -> (int, dict):
        departments = Department.objects
        if area:
            area = Polygon(area)
            departments = departments.filter(area__intersects=area)
        departments = departments.all()
        response_array = []
        for department in departments:
            response_array += [department.as_dict()]
        return 200, response_array

    @staticmethod
    def add_airboss(name, airboss_id) -> (int, dict):
        department = Department.objects.filter(name=name).first()
        if not department:
            return 400, {'message': 'No department of that name exists.'}

        airboss = User.objects.filter(id=airboss_id).first()
        if not airboss:
            return 400, {'message': 'No user of that id exists.'}
        if department.airbosses.filter(id=airboss_id).exists():
            return 400, {'message': 'This user is already an airboss for this department.'}
        department.airbosses.add(airboss)
        return 200, {'message': 'Members successfully added.'}

    @staticmethod
    def remove_airboss(name, airboss_id) -> (int, dict):
        department = Department.objects.filter(name=name).first()
        if not department:
            return 400, {'message': 'No department of that name exists.'}

        airboss = User.objects.filter(id=airboss_id).first()
        if not airboss:
            return 400, {'message': 'No user of that id exists.'}
        if not department.airbosses.filter(id=airboss_id).exists():
            return 400, {'message': 'This user is not currently an airboss for this department.'}
        department.airbosses.remove(airboss)
        return 200, {'message': 'Members successfully removed.'}

    @staticmethod
    def add_watch_commander(name, watch_commander_id) -> (int, dict):
        department = Department.objects.filter(name=name).first()
        if not department:
            return 400, {'message': 'No department of that name exists.'}

        watch_commander = User.objects.filter(id=watch_commander_id).first()
        if not watch_commander:
            return 400, {'message': 'No user of that id exists.'}
        if department.airbosses.filter(id=watch_commander_id).exists():
            return 400, {'message': 'This user is already a watch commander for this department.'}
        department.watchCommanders.add(watch_commander)
        return 200, {'message': 'Members successfully added.'}

    @staticmethod
    def remove_watch_commander(name, watch_commander_id) -> (int, dict):
        department = Department.objects.filter(name=name).first()
        if not department:
            return 400, {'message': 'No department of that name exists.'}

        watch_commander = User.objects.filter(id=watch_commander_id).first()
        if not watch_commander:
            return 400, {'message': 'No user of that id exists.'}
        if not department.watchCommanders.filter(id=watch_commander_id).exists():
            return 400, {'message': 'This user is not currently an airboss for this department.'}
        department.watchCommanders.remove(watch_commander)
        return 200, {'message': 'Members successfully added.'}

    @staticmethod
    def flight_histogram(department_id, start_day, end_day, user) -> (int, dict):
        number_of_days = (end_day-start_day).days + 1
        histogram = []
        department = Department.objects.filter(id=department_id).first()
        if not department:
            return 400, {'message': 'No department with that id exists.'}
        for index in range(0, number_of_days):
            starts_at = start_day + datetime.timedelta(days=index)
            ends_at = start_day + datetime.timedelta(days=index+1)
            num_flights = Flight.objects.filter(area__intersects=department.area, starts_at__gt=starts_at, ends_at__lt=ends_at).count()
            histogram += [num_flights]
        return 200, histogram

    @staticmethod
    def message_pilots(department_name, message):
        _now = timezone.now()
        department = Department.objects.filter(name=department_name).first()
        local_pilots = User.objects.filter(flight__area__intersects=department.area, flight__ends_at__gt=_now)\
            .distinct()
        for pilot in local_pilots:
            DepartmentTasks.email_jurisdiction.delay(pilot.username, pilot.email, department.name, message)

    @staticmethod
    def get_user_department_query(user):
        return Department.objects.filter(Q(airbosses__in=[user]) | Q(watchCommanders__in=[user])).distinct()

    @staticmethod
    def get_user_department(user) -> (int, dict):
        departments_query = DepartmentController.get_user_department_query(user)
        departments = [x.as_dict() for x in departments_query]
        return 200, departments

    @staticmethod
    def is_department_member(user):
        return bool(DepartmentController.get_user_department_query(user))

    @staticmethod
    def can_edit(user, flight):
        can_edit = False
        for department in DepartmentController.get_user_department_query(user):
            if flight.area.intersects(department.area) and user in department.airbosses.all():
                can_edit = True
        return can_edit

    @staticmethod
    def info(department_id) -> (int, dict):
        department = Department.objects.filter(id=department_id).first()
        if not department:
            return 400, {'message': 'No department with this id exists.'}
        return 200, department.as_dict()

    @staticmethod
    def delete(department_id) -> (int, dict):
        department = Department.objects.filter(id=department_id).first()
        if not department:
            return 400, {'message': 'No department with this id exists.'}
        department.delete()
        return 200, {'message': 'Department successfully deleted.'}
