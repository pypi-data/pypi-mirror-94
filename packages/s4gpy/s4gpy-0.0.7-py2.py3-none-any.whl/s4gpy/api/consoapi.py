class ConsoAPI:
    """This class wraps the conso-api."""

    def __init__(self, session):
        """Initialize a new ConsoAPI.

        It works by inheriting from the session object of a S4GAPI.
        """
        self.session = session

    def create_direct_schedule(self, airing_time, video_id):
        """Publish or updated a new direct schedule."""
        self.session.post('/direct',
            json=[{'airing_time': airing_time, 'video_id': video_id}])
