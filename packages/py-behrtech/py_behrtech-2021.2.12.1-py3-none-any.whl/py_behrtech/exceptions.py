
from requests import Response


def check_status_code(req: Response, messages: dict = None):
    """
    Check status code of requests response to raise the correct exception

    :param req: The requests Response of your requests call
    :param messages: Custom messages for error codes
    """

    if messages is None:
        messages = {}
    if req.status_code == 400:
        raise QueryError(
            status_code=400, url=req.url,
            message="Endpoint is invalid or was built incorrectly" if 400 not in messages else messages[400]
        )
    elif req.status_code == 401:
        raise JWTError(
            status_code=401,
            message="Missing JWT Access token or invalid credentials provided" if 401 not in messages else messages[401]
        )
    elif req.status_code == 403:
        raise PermissionsError(
            status_code=403,
            message="User doesn't have the correct permissions" if 403 not in messages else messages[403]
        )
    elif req.status_code == 404:
        raise QueryError(
            status_code=404, url=req.url,
            message="Endpoint is invalid or was built incorrectly" if 404 not in messages else messages[404]
        )
    elif req.status_code == 424:
        raise DependencyError(
            status_code=424,
            message="The request could not be performed because the requested action depends on another action and "
                    "that action failed." if 424 not in messages else messages[424]
        )
    elif req.status_code == 500:
        raise InternalServerError(
            status_code=500,
            message="Internal server error from the API" if 500 not in messages else messages[500]
        )


class PyBehrtechException(Exception):
    """Base exception used by this module."""
    pass


class JWTError(PyBehrtechException):
    """A request for the JWT failed"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        PyBehrtechException.__init__(self, status_code, message)


class PermissionsError(PyBehrtechException):
    """User of request doesn't have permissions"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        PyBehrtechException.__init__(self, status_code, message)


class QueryError(PyBehrtechException):
    """Request to endpoint is invalid or was built incorrectly"""

    def __init__(self, status_code, url, message):
        self.status_code = status_code
        self.url = url
        PyBehrtechException.__init__(self, status_code, url, message)


class DependencyError(PyBehrtechException):
    """Failed dependency, the request could not be preformed"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        PyBehrtechException.__init__(self, status_code, message)


class InternalServerError(PyBehrtechException):
    """Internal Server Error from the API"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        PyBehrtechException.__init__(self, status_code, message)
