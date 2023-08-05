from munch import munchify

from s4gpy.api.utils import expand_links


class DirectAPI(object):
    """This class wraps the direct API"""

    def __init__(self, session):
        """Initialize a new DirectAPI.

        It works by inheriting from the session object of a S4GAPI.
        """
        self.session = session

    def get_direct_schedule(self):
        schedules = self.session.get("/api/direct").json()
        for sche in schedules:
            expand_links(self.session, sche)

        return munchify(schedules)
