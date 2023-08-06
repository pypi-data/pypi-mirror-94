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
from typing import Tuple

from gql import (
    Client,
    gql,
)
from qctrlcommons.exceptions import QctrlGqlException

from .base import BaseQuery

CREATE_TOKENS = gql(
    """
    mutation createUserToken($username: String!, $password: String!){
        createToken (
            input: {
                username: $username
                password: $password
            }
        )
        {
            token {
                access
                refresh
            }
            errors {
                message
                fields
            }
        }
    }
    """
)


class CreateTokenQuery(BaseQuery):
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

    def __call__(self, username: str, password: str) -> Tuple[str, str]:
        """Executes the createToken mutation.

        Parameters
        ----------
        username: str
            The username used for authentication.
        password: str
            The password used for authentication.

        Returns
        -------
        tuple
            A tuple containing access_token and refresh_token respectively.

        Raises
        ------
        QctrlGqlException
            If something wrong happens with the query or authentication.
        """

        result = self.execute_query(
            CREATE_TOKENS,
            variable_values={"username": username, "password": password},
        )

        if result.get("errors"):
            raise QctrlGqlException(result["errors"])

        # custom errors handling
        if result["createToken"]["errors"]:
            raise QctrlGqlException(result["createToken"]["errors"])

        token_obj = result["createToken"]["token"]
        access_token = token_obj["access"]
        refresh_token = token_obj["refresh"]
        return access_token, refresh_token
