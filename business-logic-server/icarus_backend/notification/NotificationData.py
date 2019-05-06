from users.models import IcarusUser as User


class NotificationData:

    def __init__(self, notification_id, actor_object_id, actor_object_username, recipient_id, verb, level,
                 unread, action_object_object_id=None):
        self.actor_object_id = actor_object_id
        self.actor_object_username = actor_object_username
        self.recipient_id = recipient_id
        self.verb = verb
        self.level = level
        self.unread = unread
        self.action_object_object_id = action_object_object_id
        self.notification_id = notification_id

    def to_dict(self):
        notification_dict = dict()
        notification_dict['actor_object_id'] = self.actor_object_id
        notification_dict['actor_object_username'] = self.actor_object_username
        notification_dict['recipient_id'] = self.recipient_id
        notification_dict['verb'] = self.verb
        notification_dict['level'] = self.level
        notification_dict['unread'] = self.unread
        notification_dict['action_object_object_id'] = self.action_object_object_id
        notification_dict['id'] = self.notification_id
        return notification_dict
