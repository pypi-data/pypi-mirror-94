"""Manages a Matchlight API connection."""
from __future__ import absolute_import

import os

import logging
import requests
import requests.adapters
import requests.exceptions
import requests.packages.urllib3 as requests_urllib3

import matchlight.error


__all__ = (
    'Connection',
    'MATCHLIGHT_API_URL_V3',
)

logger = logging.getLogger('python-matchlight-sdk')

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

fileHandler = logging.FileHandler("python_matchlight_sdk.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

logger.setLevel(logging.INFO)

MATCHLIGHT_API_URL_V3 = 'https://apiv3.ml.terbiumlabs.com'


class Connection(object):
    """Matchlight API connection object."""

    def __init__(self, access_key=None, secret_key=None, https_proxy=None,
                 insecure=False, endpoint=None, search_endpoint=None):
        """Initializes a new API connection.

        Args:
            access_key (str): The user's Matchlight Public
                API access key. If not passed as an argument this value
                must be set using the ``MATCHLIGHT_ACCESS_KEY``
                environment variable.
            secret_key (str, optional): The user's Matchlight Public
                API access key. If not passed as an argument this value
                must be set using the ``MATCHLIGHT_SECRET_KEY``
                environment variable.
            https_proxy (str): A string defining the HTTPS proxy to
                use. Defaults to None.
            insecure (bool, optional): Whether or not to verify
                certificates for the HTTPS proxy. Defaults to ``False``
                (certificates will be verified).
            endpoint (str, optional): Base URL for requests. Defaults
                to ``'https://z1rw2imnti.execute-api.us-east-1.amazonaws.com/dev'``.
            search_endpoint (str, optional): Base URL for all search
                API requests.

        """
        if access_key is None:
            access_key = os.environ.get('MATCHLIGHT_ACCESS_KEY', None)
        if secret_key is None:
            secret_key = os.environ.get('MATCHLIGHT_SECRET_KEY', None)
        if access_key is None or secret_key is None:
            raise matchlight.error.SDKError(
                'The APIConnection object requires your Matchlight '
                'API access_key and secret_key either be passed as input '
                'parameters or set in the MATCHLIGHT_ACCESS_KEY and '
                'MATCHLIGHT_SECRET_KEY environment variables.')
        if endpoint is None:
            endpoint = MATCHLIGHT_API_URL_V3
        if search_endpoint is None:
            search_endpoint = MATCHLIGHT_API_URL_V3

        self.access_key = access_key
        self.secret_key = secret_key
        self.proxy = {'https': https_proxy}
        self.insecure = insecure
        self.endpoint = endpoint
        self.search_endpoint = search_endpoint
        self.session = requests.Session()
        self.session.mount(
            self.endpoint,
            requests.adapters.HTTPAdapter(
                max_retries=requests_urllib3.util.Retry(
                    total=5, status_forcelist=[500, 502, 503, 504])),
        )

    def request(self, path, data=None, endpoint=None, **kwargs):
        """Send an HTTP request to the Matchlight API.

        Args:
            path (str): The path of request URL without the URL base.
                e.g. ``/search``.
            data (dict or list): Serializable data for ``POST``
                requests. Defaults to ``None``.
            endpoint (str, optional): option to pass a different endpoint for
                each request. Defaults to Connection().endpoint

        Returns:
            A :class:`requests.models.Response` object.

        Raises:
            ConnectionError: Raised when there is an ``RetryError`` or
                ``ConnectionError`` from ``requests``.
            APIError: Raised when API does not return a 200, including
                error and custom message, if available.

        """
        # Allows SDK to use different endponts for search
        if endpoint is None:
            endpoint = self.endpoint
        url = ''.join([endpoint, path])

        method = 'GET' if data is None else 'POST'
        if 'timeout' not in kwargs:
            # API timeout is 90s
            kwargs['timeout'] = 91.0

        # response = self._request(
        response = self._pub_request(
            method,
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Matchlight-Request-Source': 'python-sdk',
                'Matchlight-Request-Source-Version': matchlight.__version__,
                'X-Matchlight-Auth': '{}:{}'.format(self.access_key, self.secret_key),
            },
            auth=(self.access_key, self.secret_key),
            proxies=self.proxy,
            verify=not self.insecure,
            **kwargs)
        return response

    def public_request(self, path, data=None, endpoint=None, method=None, params=None, **kwargs):
        """Send an HTTP request to the Matchlight API.

        Args:
            params: query parameters required
            method: different method types GET, POST, DELETE
            path (str): The path of request URL without the URL base.
                e.g. ``/search``.
            data (dict or list): Serializable data for ``POST``
                requests. Defaults to ``None``.
            endpoint (str, optional): option to pass a different endpoint for
                each request. Defaults to Connection().endpoint

        Returns:
            A :class:`requests.models.Response` object.

        Raises:
            ConnectionError: Raised when there is an ``RetryError`` or
                ``ConnectionError`` from ``requests``.
            APIError: Raised when API does not return a 200, including
                error and custom message, if available.

        """
        # Allows SDK to use different endponts for search
        if endpoint is None:
            endpoint = self.endpoint
        url = ''.join([endpoint, path])
        print(f"URL: {url}")
        method = method if method else 'GET' if data is None else 'POST'
        if 'timeout' not in kwargs:
            # API timeout is 90s
            kwargs['timeout'] = 91.0

        response = self._pub_request(
            method,
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Matchlight-Request-Source': 'python-sdk',
                'Matchlight-Request-Source-Version': matchlight.__version__,
                'X-Matchlight-Auth': '{}:{}'.format(self.access_key, self.secret_key),
            },
            auth=(self.access_key, self.secret_key),
            params=params,
            proxies=self.proxy,
            verify=not self.insecure,
            **kwargs)
        return response

    def _pub_request(self, method, url, data=None, params=None, headers=None, **kwargs):
        try:
            logger.info("Request is Method:{0}, URL:{1}, data:{2}, headers: {3}".format(method, url, data, headers))
            print("request payload: ", data)
            print("request params: ", params)
            if method == "POST":
                response = requests.post(url=url, data=data, headers=headers, params=params)
            elif method == "DELETE":
                response = requests.delete(url=url, data=data, headers=headers)
            else:
                response = requests.get(url=url, headers=headers, params=params)

            logger.info("Response: {0}".format(response.json()))

            if response.status_code == 200:
                print(response.json())
                print(response.url)
                return response
            else:
                try:
                    data = response.json()
                except ValueError:
                    data = None
                raise matchlight.error.APIError(
                    response.status_code, data)

        except requests.exceptions.RetryError:
            raise matchlight.error.ConnectionError(
                'Matchlight API request failed with too many retries')
        except requests.exceptions.ConnectionError:
            raise matchlight.error.ConnectionError(
                'Matchlight API request failed with connection error')

    def _request(self, method, url, data=None, **kwargs):
        try:
            print("request payload: ", data)
            response = self.session.request(method, url, data=data, **kwargs)
            if response.status_code == 200:
                return response
            else:
                try:
                    data = response.json()
                except ValueError:
                    data = None
                raise matchlight.error.APIError(
                    response.status_code, data)
        except requests.exceptions.RetryError:
            raise matchlight.error.ConnectionError(
                'Matchlight API request failed with too many retries')
        except requests.exceptions.ConnectionError:
            raise matchlight.error.ConnectionError(
                'Matchlight API request failed with connection error')

    def __repr__(self):  # pragma: no cover
        return self.access_key
