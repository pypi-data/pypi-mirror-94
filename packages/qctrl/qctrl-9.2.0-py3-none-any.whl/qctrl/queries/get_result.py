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
from typing import Union

from gql import Client
from graphql import GraphQLType
from qctrlcommons.exceptions import QctrlGqlException

from qctrl.builders.custom_environment import QctrlGraphQLEnvironment

from .base import BaseQuery

LOGGER = logging.getLogger(__name__)


class GetResult(BaseQuery):  # pylint:disable=too-few-public-methods
    """This class is used to retrieve the results of a previously run `function`.
    If the function is still running it will wait until it's finished
    before returning the results."""

    def __init__(
        self, client: Client, env: QctrlGraphQLEnvironment, action_id: Union[str, int]
    ):
        """
        Parameters
        ----------
        client: Client
            the graphql client
        env: QctrlGraphQLEnvironment
            the GraphQL environment object
        action_id: str
            the id an existing action
        """
        super().__init__(client, env)
        self._action_id = action_id

    def get_mutation_result_type(self, mutation_name: str) -> GraphQLType:
        """Returns the GraphQLType for the given mutation.

        Parameters
        ----------
        mutation_name : str
            The name of the mutation field in the schema.


        Returns
        -------
        GraphQLType
            Result type of the mutation

        Raises
        ------
        KeyError
            invalid mutation name.
        """
        mutation_type = self._client.schema.get_type("Mutation")
        assert mutation_type

        try:
            mutation_field = mutation_type.fields[mutation_name]
        except KeyError as error:
            raise KeyError(f"unknown mutation: {mutation_name}") from error

        return mutation_field.type

    def __call__(self) -> "qctrl.dynamic.types.CoreActionResult":
        """Executes a query and returns an instance of a CoreActionResult derived class.

        Returns
        -------
        CoreActionResult
            an instance of a `CoreActionResult` derived class.

        Raises
        ------
        QctrlGqlException
            if there's something wrong happen.
        """

        query = (
            """
            query {
                action(modelId: "%s") {
                    action {
                        ... on CoreAction {
                            mutationName
                        }
                    }
                    errors {
                        message
                    }
                }
            }
        """
            % self._action_id
        )
        LOGGER.debug("query: %s", query)

        response = self.execute_query(query)
        if response["action"].get("errors"):
            raise QctrlGqlException(
                response["action"].get("errors"), format_to_snake=True
            )
        mutation_name = response["action"]["action"].get("mutationName")
        field_type = self.get_mutation_result_type(mutation_name)

        refresh_query = self._env.build_refresh_query(field_type, self._action_id)
        response = self.execute_query(refresh_query)
        result = self._env.load_data(field_type, response["coreAction"]["coreAction"])
        self._env.wait_for_completion(field_type, result, refresh_query)
        return result
