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
from abc import (
    ABC,
    abstractmethod,
)
from typing import Union

from gql import (
    Client,
    gql,
)
from gql.transport.exceptions import TransportQueryError
from graphql import DocumentNode
from qctrlcommons.exceptions import QctrlGqlException

from qctrl.builders.custom_environment import QctrlGraphQLEnvironment


class BaseQuery(ABC):
    """Base class for a GraphQL query."""

    def __init__(self, client: Client, env: QctrlGraphQLEnvironment):
        self._client = client
        self._env = env

    def execute_query(
        self, query: Union[str, DocumentNode], **execution_params
    ) -> dict:
        """Executes a GraphQL query.

        Parameters
        ----------
        query : str or DocumentNode
            The GraphQL query to be executed.
        execution_params: dict
            input args for the query.

        Returns
        ------
        dict
            query result.

        Raises
        ------
        QctrlGqlException
            If there is an issue with the query on the Transport layer.
        """
        if isinstance(query, str):
            query = gql(query)

        try:
            return self._client.execute(query, **execution_params)
        except TransportQueryError as exc:
            raise QctrlGqlException(exc.errors) from exc

    @abstractmethod
    def __call__(self):
        raise NotImplementedError
