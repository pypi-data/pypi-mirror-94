"""Software development kit for the Terbium Labs Matchlight product."""
from __future__ import absolute_import

import pkg_resources

from .alert import Alert, AlertMethods
from .assets import AssetMethods, Asset
from .connection import Connection, MATCHLIGHT_API_URL_V3
from .error import (
    APIError,
    ConnectionError,
    InvalidCredentialsError,
    SDKError,
)
from .matches import MatchMethods

__all__ = (
    'Alert',
    'AlertMethods',
    'APIError',
    'Connection',
    'MATCHLIGHT_API_URL_V3',
    'ConnectionError',
    'InvalidCredentialsError',
    'Matchlight',
    'SDKError',
)


try:
    __version__ = pkg_resources.get_distribution('matchlightsdk').version
except:
    __version__ = 'unknown'


class Matchlight(object):
    """Top-level Matchlight API connection object.

    A top-level wrapper for all Matchlight products: including
    Retrospective Search, DataFeeds, and Fingerprint Monitoring
    (projects, and records).

    Attributes:
        alerts: :class:`~matchlight.alert.AlertMethods` object
            with access to alert methods for Matchlight Fingerprint
            Monitoring.
        projects: :class:`~matchlight.project.ProjectMethods` object
            with access to project methods for Matchlight Fingerprint
            Monitoring.
        records: :class:`~matchlight.record.RecordMethods` object with
            access to record methods for Matchlight Fingerprint
            Monitoring.
        feeds: :class:`~matchlight.feed.FeedMethods` object with access
            to all Matchlight DataFeed methods.
        search: :class:`~matchlight.search.SearchMethods` object with
            access to Matchlight Retrospective Search.

    """

    def __init__(self, access_key=None, secret_key=None, **kwargs):
        """Matchlight API connection object.

        This class is a wrapper over the Matchlight API feature set
        including functionality for search, feeds, projects, and
        records.

        Attributes:
            access_key (str, optional): The user's Matchlight API
                access key. If not passed as an argument this value
                must be set using the ``MATCHLIGHT_ACCESS_KEY``
                environment variable.
            secret_key (str, optional): The user's Matchlight API
                access key. If not passed as an argument this value
                must be set using the ``MATCHLIGHT_SECRET_KEY``
                environment variable.

        """
        self.conn = Connection(
            access_key=access_key, secret_key=secret_key, **kwargs)
        self.alerts = AlertMethods(self.conn)
        self.assets = AssetMethods(self.conn)
        self.matches = MatchMethods(self.conn)
