"""Helper utilities and decorators."""
import hashlib
import socket
from typing import Optional
from urllib.parse import urlparse

import requests


class IPInfo:
    HOST = "ipinfo.io"
    BASE_URL = "https://{}".format(HOST)

    def __init__(self):
        self.session = requests.Session()

    def basic(self, ip_address: str) -> dict:
        url = "{}/{}/".format(self.BASE_URL, ip_address)
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def geo(self, ip_address: str) -> dict:
        url = "{}/{}/geo".format(self.BASE_URL, ip_address)
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    @classmethod
    def get_geo(cls, ip_address: str) -> dict:
        instance = cls()
        return instance.geo(ip_address)

    @classmethod
    def get_basic(cls, ip_address: str) -> dict:
        instance = cls()
        return instance.basic(ip_address)


def get_hostname_from_url(url: str) -> Optional[str]:
    """Get a hostname from a URL

    Arguments:
        url {str} -- URL

    Returns:
        Optional[str] -- A hostname, returns None if an invalid input is given
    """
    parsed = urlparse(url)
    if parsed.netloc == "":
        return None
    return parsed.netloc


def get_ip_address_by_hostname(hostname: str) -> Optional[str]:
    """Get an IP address by a hostname

    Arguments:
        hostname {str} -- Hostname

    Returns:
        Optional[str] -- An IP address, returns None if an error occurs
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        return None


def get_country_code_by_ip_address(ip_address: str) -> Optional[str]:
    try:
        json = IPInfo.get_geo(ip_address)
        return json.get("country")
    except Exception:
        return None


def get_asn_by_ip_address(ip_address: str) -> Optional[str]:
    """Get ASN by an IP address

    Arguments:
        ip_address {str} -- IP address

    Returns:
        Optional[str] -- ASN as a string, returns None if an error occurs
    """
    try:
        json = IPInfo.get_basic(ip_address)
        return json.get("org")
    except Exception:
        return None


def calculate_sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
