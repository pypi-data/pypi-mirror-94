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
from functools import lru_cache
from typing import (
    Any,
    List,
)

import inflection
from gql import (
    Client,
    gql,
)
from graphql import (
    DocumentNode,
    GraphQLNonNull,
    GraphQLType,
)
from tqdm.auto import tqdm

from .async_result import AsyncResult
from .custom_handlers import (
    ComplexArrayEntryHandler,
    ComplexArrayHandler,
    ComplexArrayInputHandler,
    ComplexDenseArrayHandler,
    ComplexNumberHandler,
    ComplexNumberInputHandler,
    ComplexSparseArrayHandler,
    DateTimeScalarHandler,
    GraphScalarHandler,
    JsonDictScalarHandler,
    JsonStringScalarHandler,
    UnixTimeScalarHandler,
)
from .graphql_utils import (
    BaseHandler,
    GraphQLEnvironment,
)
from .type_registry import TypeRegistry
from .wait import Wait

LOGGER = logging.getLogger(__name__)


class QctrlGraphQLEnvironment(GraphQLEnvironment):
    """
    Custom GraphQLEnvironment class.
    """

    _action_selection_override = {
        "action": r"{ modelId name status errors { exception } progress }"
    }

    refresh_parameters = (
        "{ action { modelId name status errors { exception } progress result } "
        "errors { fields message } }"
    )

    def __init__(
        self,
        gql_client: Client,
        type_registry_cls: type = None,
        custom_handlers: List[BaseHandler] = None,
    ):
        self._gql_client = gql_client
        super().__init__(type_registry_cls, custom_handlers)

    @lru_cache()
    def field_to_attr(self, field_name: str) -> str:
        """Uses inflection to convert a GraphQL
        field name to an attribute name.

        Parameters
        ----------
        field_name : str
            The name of the GraphQL field.

        Returns
        -------
        str
            attribute name
        """
        return inflection.underscore(field_name)

    def build_mutation_query(
        self,
        mutation_name: str,
        input_type: GraphQLType,
        result_type: GraphQLType,
        data: Any,
    ) -> DocumentNode:
        """Returns the corresponding GraphQL mutation query."""
        payload = self.format_payload(input_type, data)
        selection = self.get_selection(result_type, self._action_selection_override)

        query = (
            f"mutation startAction {{{mutation_name}(input: {payload}) {selection}}}"
        )
        LOGGER.debug("query:%s", query)
        return gql(query)

    def wait_for_completion(
        self, field_type: GraphQLType, obj: Any, refresh_query: DocumentNode
    ):
        """Waits until the corresponding action is completed on the server."""
        _wait = Wait()

        with tqdm(total=100, leave=False) as progress_bar:
            _total = 0
            async_result = AsyncResult(
                self._gql_client, obj, progress_bar, refresh_query
            )

            while not obj.is_completed:
                progress = int(obj.progress * 100) - _total
                _total += progress
                progress_bar.update(progress)
                _wait()
                result = async_result.refresh()
                self.update_data(field_type, obj, result)
                async_result.write_waiting_message()

            progress_bar.update(max(0, progress_bar.total - progress_bar.n))

        # action is now completed
        if not obj.is_successful:
            if obj.job_errors:
                raise RuntimeError(f"Execution failed: {obj.job_errors.exception}")

            if obj.status == obj.FAILURE:
                raise RuntimeError(
                    "Execution resulted with status 'FAILURE'("
                    "no extra details about the errors are "
                    "available)."
                )

        LOGGER.info(
            "Action %s finished with status: %s", str(obj.action_id), obj.status
        )

    def build_refresh_query(
        self, field_type: GraphQLType, action_id: int
    ) -> DocumentNode:
        """Returns a GraphQL query to select data for
        refreshing an object populated with response data.
        """

        if isinstance(field_type, GraphQLNonNull):
            field_type = field_type.of_type

        selection = self.refresh_parameters
        query = (
            """
        query refreshAction {{
            coreAction(modelId: "{action_id}") {{
                coreAction {{
                    ... on {field_type} {selection}
                }}
                errors {{
                    message
                    fields
                }}
            }}
        }}"""
        ).format(
            action_id=action_id,
            field_type=field_type.name,
            selection=selection,
        )

        LOGGER.debug("query:%s", query)
        return gql(query)


def create_environment(gql_client: Client) -> QctrlGraphQLEnvironment:
    """Creates the custom environment object with
    all custom handlers.
    """
    return QctrlGraphQLEnvironment(
        gql_client=gql_client,
        type_registry_cls=TypeRegistry,
        custom_handlers=[
            ComplexArrayEntryHandler,
            ComplexArrayHandler,
            ComplexArrayInputHandler,
            ComplexDenseArrayHandler,
            ComplexNumberHandler,
            ComplexNumberInputHandler,
            ComplexSparseArrayHandler,
            JsonStringScalarHandler,
            DateTimeScalarHandler,
            GraphScalarHandler,
            JsonDictScalarHandler,
            UnixTimeScalarHandler,
        ],
    )
