from users.models import IcarusUser as User
from .NotificationDTO import NotificationDTO
from notifications.models import Notification


class NotificationController:

    @staticmethod
    def unread(user) -> (int, dict):
        user = User.objects.get(pk=user.pk)
        notification_db_query = user.notifications.unread()
        notification_data_list = NotificationDTO.db_query_to_data(notification_db_query)
        notification_data_dict = [x.to_dict() for x in notification_data_list]
        return 200, notification_data_dict

    @staticmethod
    def read_all(user) -> (int, dict):
        user = User.objects.get(pk=user.pk)
        user.notifications.mark_all_as_read()
        return 200, {'message': 'All successfully marked as read.'}

    @staticmethod
    def read(notification_id):
        notification = Notification.objects.filter(id=notification_id).first()
        if not notification:
            return 400, {'message': 'Bad notification id.'}
        notification.mark_as_read()
        return 200, {'message': 'Message successfully marked as read.'}

    @staticmethod
    def feed(user, count) -> (int, dict):
        if not count:
            return 400, {'message': 'Count is not provided.'}
        count = int(count)
        if not count:
            return 400, {'message': 'Count is not an integer.'}
        user = User.objects.get(pk=user.pk)
        notification_db_query = user.notifications.all().order_by('-id')[:count]
        notification_data_list = NotificationDTO.db_query_to_data(notification_db_query)
        notification_data_dict = [x.to_dict() for x in notification_data_list]
        return 200, notification_data_dict
