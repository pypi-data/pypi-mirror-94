# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
# pylint:disable=missing-module-docstring
import logging
import os
from threading import Thread
from typing import Dict

import pythonflow as pf
import tenacity
from gql import (
    Client,
    gql,
)
from qctrlcommons.exceptions import QctrlException
from requests.exceptions import (
    BaseHTTPError,
    RequestException,
)

from .builders import (
    build_namespaces,
    create_client_auth,
    create_environment,
    create_gql_client,
    validate_client_auth,
)
from .constants import DEFAULT_API_ROOT
from .queries import (
    ActivityMonitor,
    GetResult,
)
from .utils import _check_qctrl_latest_version

LOGGER = logging.getLogger(__name__)


class Qctrl:
    """A mediator class. Used to authenticate with Q-CTRL and access Q-CTRL features.

    Creating an instance of this class requires authentication with Q-CTRL's API.

    The recommended method of authentication is through the interactive authentication
    method. This method can be invoked by simply calling Qctrl() without any arguments.
    This method will also create an authentication file that will be used for subsequent
    authentications when using the package.

    .. code-block:: python

      q = Qctrl()

    If needed authentication can also be done by passing your email and password as arguments
    to the Qctrl() function as shown below. Ensure that the credentials used are secure.

    .. code-block:: python

      q = Qctrl(email='myemail', password='mypassword')

    Parameters
    ----------
    email : str, optional
        The email address for a Q-CTRL account. (Default value = None)
    password : str, optional
        The password for a Q-CTRL account. (Default value = None)
    api_root : str, optional
        The URL of the Q-CTRL API. (Default value = None)
    skip_version_check: bool, optional
        option for disabling the version check. ( Default value = False)


    Attributes
    ----------
    functions : qctrl.dynamic.namespaces.FunctionNamespace
    operations : qctrl.dynamic.namespaces.OperationNamespace
    types : qctrl.dynamic.namespaces.TypeNamespace


    Raises
    ------
    QctrlApiException
    """

    gql_api = None
    functions = None
    operations = None
    types = None

    def __init__(
        self,
        email: str = None,
        password: str = None,
        api_root: str = None,
        skip_version_check: bool = False,
    ):
        if not skip_version_check:
            self._check_version_thread()
        self._api_root = (
            api_root or os.environ.get("QCTRL_API_HOST") or DEFAULT_API_ROOT
        )
        assert self._api_root

        self.gql_api = self._build_client(email, password)
        self.gql_env = create_environment(self.gql_api)
        self._build_namespaces()

    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=5),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_exception_type((RequestException, BaseHTTPError)),
    )
    def _build_client(self, email: str = None, password: str = None) -> Client:
        """
        Builds the GraphQL client.

        Parameters
        ----------
        email: str
            user email (Default value = None)
        password: str
            user password (Default value = None)

        Returns
        -------
        Client
            gql client.
        """
        auth = create_client_auth(self._api_root, email, password)
        client = create_gql_client(self._api_root, auth)
        validate_client_auth(client)
        return client

    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=5),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_exception_type((RequestException, BaseHTTPError)),
    )
    def _build_namespaces(self):
        """Builds the dynamic namespaces."""
        (
            self.functions,
            self.operations,
            self.types,
        ) = build_namespaces(self)

    @staticmethod
    def create_graph():
        """
        Creates a graph object.
        """
        return pf.Graph()

    def activity_monitor(
        self,
        limit: int = 5,
        offset: int = 0,
        status: str = None,
        action_type: str = None,
    ) -> None:
        """Prints a list of previously run actions to the console
        and their statuses. Allows users to filter the amount of
        actions shown as well as provide an offset.

        Parameters
        ----------
        limit : int
            The number of previously ran actions to show.(Default is 5)
        offset : int
            Offset the list of actions by a certain amount.
        status : str
            The status of the action.
        action_type : str
            The action type.


        Returns
        -------
        None
            instead of returning a query. It will print out the formatted query result.
        """

        query = ActivityMonitor(
            self.gql_api,
            self.gql_env,
            limit=limit,
            offset=offset,
            status=status,
            action_type=action_type,
        )
        return print(query())

    def get_result(self, action_id: str) -> "qctrl.dynamic.types.CoreActionResult":
        """This function is used to return the results of a previously run function.
        You will be able to get the id of your action from the activity monitor.

        Parameters
        ----------
        action_id: str
            the id of the action which maps to an executed function.

        Returns
        -------
        qctrl.dynamic.types.CoreActionResult
            an instance of a class derived from a CoreActionResult.
        """
        get_result = GetResult(self.gql_api, self.gql_env, action_id=action_id)
        return get_result()

    def _run_gql_query(self, query: str, variable_values: Dict = None) -> Dict:
        """
        Runs a GQL query in a Python script.

        Parameters
        ----------
        query: str
            query string.
        variable_values: Dict
            Dictionary of input parameters. (Default value = None)

        Returns
        -------
        Dict
            gql response.

        Raises
        ------
        QctrlException
            if there's any root level errors
        """
        response = self.gql_api.execute(gql(query), variable_values)
        if response.get("errors"):
            raise QctrlException(response["errors"])
        return response

    @staticmethod
    def _check_version_thread():
        """
        Use another thread to check qctrl version.
        """
        thread = Thread(target=_check_qctrl_latest_version, daemon=True)
        thread.start()


__all__ = [
    "Qctrl",
]
