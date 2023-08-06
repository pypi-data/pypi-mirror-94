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
from typing import (
    Dict,
    Set,
)

from dateutil.parser import isoparse
from gql import (
    Client,
    gql,
)
from qctrlcommons.exceptions import (
    QctrlException,
    QctrlGqlException,
)

from qctrl.builders.custom_environment import QctrlGraphQLEnvironment

from .base import BaseQuery


class ActivityMonitor(BaseQuery):
    """Class for executing and formatting Activity Monitor query."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        client: Client,
        env: QctrlGraphQLEnvironment,
        limit: int = 5,
        offset: int = 0,
        status: str = None,
        action_type: str = None,
    ):
        super().__init__(client, env)
        self.limit = limit
        self.offset = offset
        self.status = status
        self.action_type = action_type
        self.validate()

    def get_enum_values(self, enum_type: str) -> Set:
        """Retrieves the enum values from the schema.

        Parameters
        ----------
        enum_type: str
            Graphql enum type name

        Returns
        -------
        Set
            enum set value.

        Raises
        ------
        TypeError
            invalid enum type name.
        """
        field_type = self._client.schema.get_type(enum_type)

        if field_type is None:
            raise TypeError(f"unknown enum_type: {enum_type}")

        return set(field_type.values.keys())

    def __call__(self) -> str:
        """Executes the actions query."""
        self.validate()
        query = gql(
            """
            query getActions($limit: Int, $offset: Int, $filterBy: ActionFilter){
                actions(limit:$limit, offset:$offset, filterBy:$filterBy){
                    actions {
                        name
                        status
                        modelType
                        progress
                        createdAt
                        updatedAt
                        modelId
                    }
                    errors {
                        message
                    }
                }
            }
            """
        )

        filter_by = {}
        if self.status:
            filter_by["status"] = {"exact": self.status}
        if self.action_type:
            filter_by["modelType"] = {"exact": self.action_type}

        params = {"limit": self.limit, "offset": self.offset, "filterBy": filter_by}
        response = self.execute_query(query, variable_values=params)
        return self.format_query_output(response)

    def validate(self):
        """Validates the query input."""
        if self.limit < 1:
            raise QctrlException("Limit cannot be less than 1.")

        if self.offset < 0:
            raise QctrlException("Offset cannot be less than 0.")

        if self.status and self.status not in self.get_enum_values("ActionStatusEnum"):
            raise QctrlException(
                f"Status '{self.status}' is not valid. "
                f"Please choose from a valid status type: "
                f"{self.get_enum_values('ActionStatusEnum')}"
            )

        if self.action_type and self.action_type not in self.get_enum_values(
            "ActionTypeEnum"
        ):
            raise QctrlException(
                f"Action type '{self.action_type}' is not valid. "
                f"Please choose from a valid action type: "
                f"{self.get_enum_values('ActionTypeEnum')}"
            )

    @staticmethod
    def format_query_output(results: Dict) -> str:
        """Formats the query output into a readable table-like manner.

        Parameters
        ----------
        results: Dict
            activity monitor raw query result.

        Returns
        -------
        str
            formatted query output.

        Raises
        ------
        QctrlGqlException
            if there's something wrong happen
        """
        if results["actions"]["errors"]:
            raise QctrlGqlException(results["actions"]["errors"], format_to_snake=True)

        actions = (
            f'{"Name":<40} '
            f'{"Status":<10} '
            f'{"Type":<40} '
            f'{"Progress":<10} '
            f'{"Created at":<24} '
            f'{"Completed at":<24} '
            f'{"Id":<10}\n'
        )
        for result in results["actions"]["actions"]:
            created_at = "{:%d-%m-%Y %H:%M:%S}".format(isoparse(result["createdAt"]))
            completed_at = "{:%d-%m-%Y %H:%M:%S}".format(isoparse(result["updatedAt"]))
            action = (
                f'\n{result["name"]:<40} '
                f'{result["status"]:<10} '
                f'{result["modelType"]:<40} '
                f'{result["progress"]:<10.0%} '
                f"{created_at:<24} "
                f"{completed_at:<24} "
                f'{result["modelId"]:<10}\n'
            )
            actions = actions + action

        return actions
