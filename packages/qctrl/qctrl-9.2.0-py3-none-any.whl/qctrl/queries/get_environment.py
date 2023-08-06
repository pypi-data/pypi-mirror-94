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
    Any,
    Dict,
)

from gql import gql
from qctrlcommons.exceptions import QctrlGqlException

from .base import BaseQuery

get_env_query = gql(
    """
    query getEnvironment {
        environment {
            environment {
                workers {
                    name
                    queues
                    totalProcesses
                    activeTasks
                    reservedTasks
                    queuedTasks
                }
            }
            errors {
                message
            }
        }
    }
    """
)


class GetWorkerInfo(BaseQuery):
    """
    Class for executing and formatting the `environment` query to per worker view.
    """

    def __call__(self) -> str:
        """
        Executes the `getEnvironment` query.
        """
        response = self.execute_query(get_env_query)
        return self.format_query_output(response)

    @staticmethod
    def format_query_output(results: Dict) -> str:
        """
        Formats the query output into a readable table-like manner.

        Parameters
        ----------
        results : Dict
            environment raw query result.

        Returns
        -------
        str
            formatted query output.

        Raises
        ------
        QctrlGqlException
            Any handled error that occurred on the server
        """
        if results["environment"]["errors"]:
            raise QctrlGqlException(
                results["environment"]["errors"], format_to_snake=True
            )

        result = (
            f'{"Worker Name":<60} '
            f'{"Queue(s)":<30} '
            f'{"Total Processes":<20} '
            f'{"Active Tasks":<20} '
            f'{"Availability":<20} '
            f'{"Reserved Tasks":<20} '
            "\n"
        )

        for worker in results["environment"]["environment"]["workers"]:
            result += (
                "\n"
                f'{worker["name"]:<60} '
                f'{", ".join(worker["queues"]):<30} '
                f'{worker["totalProcesses"]:<20} '
                f'{worker["activeTasks"]:<20} '
                f"{_get_availability(worker):<20}"
                f'{worker["reservedTasks"]:<20}'
                "\n"
            )

        return result


class GetQueueInfo(BaseQuery):
    """Class for executing and formatting the `environment` query to per queue view."""

    def __call__(self) -> str:
        """
        Executes the actions query.
        """
        response = self.execute_query(get_env_query)
        return self.format_query_output(response)

    @staticmethod
    def format_query_output(results):
        """
        Formats the query output into a readable table-like manner.

        Parameters
        ----------
        results : Dict
            environment raw query result.

        Returns
        -------
        str
            formatted query output.

        Raises
        ------
        QctrlGqlException
            Any handled error that occurred on the server
        """
        result = (
            f'{"Queue":<60} '
            f'{"Workers":<30} '
            f'{"Total Processes":<20} '
            f'{"Active Tasks":<20} '
            f'{"Availability":<20} '
            f'{"Queued Tasks":<20} '
            "\n"
        )
        env_info = {
            "worker": 0,
            "totalProcesses": 0,
            "activeTasks": 0,
            "Availability": 0,
            "queuedTasks": 0,
        }
        queues = {}
        if results["environment"]["errors"]:
            raise QctrlGqlException(
                results["environment"]["errors"], format_to_snake=True
            )

        for worker in results["environment"]["environment"]["workers"]:
            # assume one worker belongs to one queue only
            queue = worker["queues"][0]
            if queue not in queues:
                queues.update({queue: env_info.copy()})
            queues[queue]["worker"] += 1
            queues[queue]["totalProcesses"] += worker["totalProcesses"]
            queues[queue]["activeTasks"] += worker["activeTasks"]
            queues[queue]["queuedTasks"] += worker["queuedTasks"]
            queues[queue]["Availability"] = _get_availability(queues[queue])

        for queue_name, queue_info in queues.items():
            result += (
                "\n"
                f"{queue_name:<60} "
                f'{queue_info["worker"]:<30} '
                f'{queue_info["totalProcesses"]:<20} '
                f'{queue_info["activeTasks"]:<20} '
                f'{queue_info["Availability"]:<20} '
                f'{queue_info["queuedTasks"]:<20} '
                "\n"
            )

        return result


def _get_availability(data: Dict[str, Any]) -> str:
    """
    Calculates the queue/worker availability
    based on active tasks and total processes.

    Parameters
    ----------
    data: Dict[str, Any]
        worker or queue data
    Returns
    -------
    float
        availability
    """
    num_active = float(data["activeTasks"])
    num_total = float(data["totalProcesses"])

    result = 1 - num_active / num_total
    return f"{result*100:.1f}%"
