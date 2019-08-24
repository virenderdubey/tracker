import logging
from accounts.models import User, Team

logger = logging.getLogger(__name__)

class TaskFilters(object):
    
    @classmethod
    def currentUser(self, request):
        try:
            return User.objects.get(username=request.user.username)
        except Exception as e:     # noqa
            logger.exception(e)
            return None
