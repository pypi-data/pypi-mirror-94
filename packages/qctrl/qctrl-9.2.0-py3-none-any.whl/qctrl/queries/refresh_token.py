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

from ..utils import TokenError
from .base import BaseQuery

REFRESH_TOKENS = gql(
    """
    mutation refreshUserToken($token: String!){
        refreshToken (
            input: {
                token: $token
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


class RefreshTokenQuery(BaseQuery):
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

    def __call__(self, token: str) -> Tuple[str, str]:
        """Executes the refreshToken mutation.

        Parameters
        ----------
        token: str
            A valid refresh_token to renew the JWT.

        Returns
        -------
        tuple
            A tuple containing access_token and refresh_token respectively.

        Raises
        ------
        QctrlGqlException
            If something wrong happens with the query or authentication.
        TokenError
            If there is an error with the refresh token query.
        """

        try:
            result = self.execute_query(
                REFRESH_TOKENS,
                variable_values={"token": token},
            )
        except QctrlGqlException as exc:
            raise TokenError from exc

        if result.get("errors"):
            raise QctrlGqlException(result["errors"])

        # custom errors handling
        if result["refreshToken"]["errors"]:
            raise QctrlGqlException(result["refreshToken"]["errors"])

        token_obj = result["refreshToken"]["token"]
        access_token = token_obj["access"]
        refresh_token = token_obj["refresh"]
        return access_token, refresh_token
