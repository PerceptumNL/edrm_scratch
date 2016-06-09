import requests

def get_routed_url(url, domain=None):
    from urllib.parse import urlsplit, urlunsplit
    from binascii import b2a_hex
    from subdomains.utils import get_domain
    from django.conf import settings

    parts = urlsplit(url)
    domain = parts.netloc or domain
    hashed_domain = "%s.%s" % (
        b2a_hex(bytes(domain, "utf-8")).decode("utf-8"), settings.ROUTER_DOMAIN)

    return urlunsplit((
        settings.ROUTER_PROTOCOL or parts.scheme,
        hashed_domain,
        parts.path,
        parts.query,
        parts.fragment))

class Scratch(object):
    token = None

    def __init__(self, token=None):
        self.token = token

    def _fetch_json(self, url):
        routed_url = get_routed_url(url)
        return requests.get(url).json()

    def get_projects(self):
        if self.token is None:
            return []
        else:
            return self._fetch_json(
                "https://scratch.mit.edu/site-api/projects/all/")
