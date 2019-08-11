import logging
from accounts.models import User, Team

logger = logging.getLogger(__name__)

class Filters(object):
    def currentUser(self, username):
        try:
            return User.objects.get(username=username)
        except Exception as e:     # noqa
            logger.exception(e)
            return None
