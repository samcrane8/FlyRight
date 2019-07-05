import os
from users.models import IcarusUser as User

User.objects.create_superuser(os.environ.get('SUPERUSER_USERNAME', 'password'), os.environ.get('SUPERUSER_EMAIL', 'admin@password.com'), os.environ.get('SUPERUSER_PASSWORD', 'password'))
