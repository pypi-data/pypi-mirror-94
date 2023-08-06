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
from gql import (
    Client,
    gql,
)
from qctrlcommons.exceptions import QctrlGqlException

from .base import BaseQuery

ME_QUERY = gql(
    """
    query {
        me {
            me {
                ... on User {
                    username
                }
            }
            errors {
                message
                fields
            }
        }
    }
    """
)


class MeQuery(BaseQuery):
    """
    temporary docstring
    """

    def __init__(
        self,
        client: Client,
    ):
        """
        Parameters
        ----------
        client: Client
            The graphql client.
        """
        super().__init__(client, None)

    def __call__(self) -> str:
        """Executes the refreshToken mutation.

        Returns
        -------
        str
            The user's username.

        Raises
        ------
        QctrlGqlException
            If something wrong happens with the query or authentication.
        """

        result = self.execute_query(ME_QUERY)

        if result.get("errors"):
            raise QctrlGqlException(result["errors"])

        # custom errors handling
        if result["me"]["errors"]:
            raise QctrlGqlException(result["me"]["errors"])

        username = result["me"]["me"]["username"]
        return username
