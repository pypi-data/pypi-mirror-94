from munch import munchify

from s4gpy.api.utils import expand_links

Object = lambda **kwargs: type("Object", (), kwargs)


class UserAPI:
    """This class wraps the user API"""

    def __init__(self, session):
        """intialiaze a new User API"""
        self.session = session

    def get_users(self):
        """returns a list of users."""
        users = self.session.get("/api/users").json()
        for user in users:
            expand_links(self.session, user)

        return munchify(users)

    def get_user(self, user_id):
        """get information about a particular user."""
        return munchify(self.session.get(f"/api/user/{user_id}").json())
