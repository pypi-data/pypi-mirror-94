"""Stream4good/Discoverability API Wrapper."""
import requests

from s4gpy.api.direct import DirectAPI
from s4gpy.api.consoapi import ConsoAPI
from s4gpy.api.credentials import CredentialAPI
from s4gpy.api.user import UserAPI
from s4gpy.s4gsession import S4GSession
from s4gpy.api.netflixapi import NetflixAPI



class S4GAPI:
    """This class wraps stream4good/discoverability Rest API."""

    def __init__(self, user,
                 password,
                 client_id='dashboard-vuejs',
                 scope='dashboard-vuejs',
                 root_dns='vod-prime.space',
                 protocol='https',
                 realm='discoverability'):
        """Create an initilize the API."""
        self.user = user
        self.password = password
        self.root_dns = root_dns
        self.protocol = protocol
        self.realm = realm
        self.access_token_url =\
            f'/auth/realms/{self.realm}/protocol/openid-connect/token'
        payload = {'client_id': client_id,
                   'grant_type': 'password',
                   'scope': scope,
                   'username': self.user,
                   'password': self.password}
        self.session = requests.Session()
        resp = self.session.post(
            f'{self.protocol}://auth.{self.root_dns}'
            + f'/auth/realms/{self.realm}'
            + '/protocol/openid-connect/token',
            data=payload)
        self.access_token = resp.json()['access_token']

    def get_credentials_api(self):
        """Returns a configured instance of CredentialAPI"""
        return CredentialAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://credentials.{self.root_dns}',
                access_token=self.access_token))

    def get_conso_api(self):
        """Return a configured instance of the ConsoAPI."""
        return ConsoAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://conso-api.{self.root_dns}',
                access_token=self.access_token))

    def get_user_api(self):
        """Return a configured instance of the ConsoAPI."""
        return UserAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://api.{self.root_dns}',
                access_token=self.access_token))
    def get_netflix_api(self):
        """Return a configured instance of the NetflixAPI."""
        return NetflixAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://api.{self.root_dns}/api/netflix',
                access_token=self.access_token))

    def get_direct_api(self):
        """Return a configured instance of the ConsoAPI."""
        return DirectAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://api.{self.root_dns}',
                access_token=self.access_token))


__all__ = [
    'S4GAPI'
]
