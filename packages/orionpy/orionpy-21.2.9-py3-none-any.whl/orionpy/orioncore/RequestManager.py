import requests
import urllib3
from sys import exit


class _Singleton(type):
    """
    metaclass of Orion.
    type is the base metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """

        :param args: list of arguments
        :param kwargs: Dictionary [keyword arguments]= values of these arguments
        :return:
        """
        # If the class was not created yet (not in our list)...
        if cls not in cls._instances:
            # call the __call__ method of type. So, calls the class constructor
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RequestManager(metaclass = _Singleton):
    """Class managing communication with the REST API.
    The only one to use the requests python library.
    """

    def __init__(self, output_format='json', token=None, verify=True):
        self._basedata = {'f': output_format}
        if not verify:
            print('[WARNING] Unverified HTTPS request is being made. '
                  'Adding certificate verification is strongly advised.')
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.verify = verify
        if token is not None:
            self._basedata['token'] = token

    def set_token(self, token):
        """Set a given token to be used in all other requests.

        :param token: token to set. Must be valid
        """
        self._basedata['token'] = token

    def get_basedata(self):
        """

        :return: basedata used for requests (token and format)
        """
        return self._basedata

    def _merge_data(self, params, keep_base_parameters):
        """Adds new parameters to the default ones"""
        if params is None and keep_base_parameters:
            params = self._basedata
        elif params is not None and keep_base_parameters:
            # merge the two dictionaries in one
            params = {**self._basedata, **params}
        return params

    def get(self, url, params=None, keep_base_parameters=True):
        """Does a GET request on the url

        :param url: where to do the requests
        :param params: parameters for the request
        :param keep_base_parameters: Boolean if want to keep default parameters.
        :return: the request's answer.
        """
        params = self._merge_data(params, keep_base_parameters)

        try:
            req = requests.get(url, params = params, verify = self.verify)
            if req.status_code != requests.codes.ok:
                req.raise_for_status()
        except requests.exceptions.HTTPError as he:
            print('HTTP error : ', he)
            exit(-1)
        return req

    def post(self, url, data=None, keep_base_parameters=True):
        """Does a POST request on the url

        :param url: where to do the requests
        :param data: parameters for the request
        :param keep_base_parameters: Boolean if want to keep default parameters.
        :return: the request's answer
        """
        data = self._merge_data(data, keep_base_parameters)
        try:
            req = requests.post(url, data = data, verify = self.verify)
            if req.status_code != requests.codes.ok:
                req.raise_for_status()
        except requests.exceptions.ConnectionError as ce:
            print('Connection error :', ce)
            print('url :', url)
            exit(-1)
        except requests.exceptions.HTTPError as he:
            print('HTTP error : ', he)
            exit(-1)
        return req

    def post_in_python(self, url, data=None, keep_base_parameters=True):
        """Does a POST request on the url and returns the answer as a Python structure

        :param url: where to do the requests
        :param data: parameters for the request
        :param keep_base_parameters: Boolean if want to keep default parameters
        :return: Request answer converted from json to python
        """
        struct = self.post(url, data, keep_base_parameters).json()
        if 'error' in struct:
            print('ERROR in response : ', struct['error'])
            print('url : ', url)
            exit(-1)
        return struct

    def get_python_answer(self, response):
        """Convert a string in json format to a python dictionary

        :param response: Answer of http request.
        :return: the json string converted in a python dictionary
        """
        struct = response.json()
        if 'error' in struct:
            print('ERROR in response : ', struct['error'])
            print('url : ', response.url)
            exit(-1)
        return struct

    def get_in_python(self, url, params=None, keep_base_parameters=True):
        """Does a get request and return the answer formatted as a Python structure

        :return: Request answer converted from json to python
        """
        # TODO use it directly instead of get_python_answer
        return self.get_python_answer(self.get(url, params, keep_base_parameters))
