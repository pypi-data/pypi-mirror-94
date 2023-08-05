class CredentialAPI():
    """Wraps credential API."""

    def __init__(self, session):
        """intialiaze a new Credential API"""
        self.session = session

    def get_credentials(self, provider):
        """Get a tuple containing credentials for the supplied provider."""
        credentials = self.session.get(f'/providers/{provider}').json()
        single_credentials_link = credentials['links'][0]['href']

        single_credentials = self.session.get(
            single_credentials_link,
        ).json()
        login = single_credentials['credentials']['login']
        password = single_credentials['credentials']['password']
        return login, password
