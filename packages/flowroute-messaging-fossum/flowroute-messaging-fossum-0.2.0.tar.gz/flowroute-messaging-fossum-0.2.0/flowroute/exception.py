# -*- coding: utf-8 -*-

"""FlowrouteMessagingLib.APIException

Copyright Flowroute, Inc. 2016
"""


class FlowrouteException(Exception):
    """Class that handles HTTP Exceptions when fetching API Endpoints.

    Attributes:
        reason (str):
            The reason (or error message) for the Exception
            to be raised.
        response_code (int):
            The HTTP Response Code from the API Request that
            caused this exception to be raised.
        response_body (str):
            The body that was retrieved during the API request.
    """

    def __init__(self, reason: str, response_code: int, response_body: str):
        Exception.__init__(self, reason)
        self.response_code = response_code
        self.response_body = response_body
