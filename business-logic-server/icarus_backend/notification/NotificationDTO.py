from .NotificationData import NotificationData
from users.models import IcarusUser as User


class NotificationDTO:

    @staticmethod
    def db_query_to_data(db_query):
        notification_data_list = []
        for db_notification in db_query:
            user = User.objects.filter(id=db_notification.actor_object_id).first()
            if user:
                username = user.username
            else:
                username = '[Deleted]'
            notification_data_list += [NotificationData(
                db_notification.id,
                db_notification.actor_object_id,
                username,
                db_notification.recipient_id,
                db_notification.verb,
                db_notification.level,
                db_notification.unread,
                db_notification.action_object_object_id,
            )]
        return notification_data_list

    @staticmethod
    def db_to_data(db_model):
        pass