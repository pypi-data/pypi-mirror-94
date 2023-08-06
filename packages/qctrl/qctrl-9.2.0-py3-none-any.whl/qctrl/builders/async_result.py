"""Module for `AsyncResult`."""
import json
from math import ceil
from typing import (
    Dict,
    Optional,
)

from gql import Client
from graphql import DocumentNode
from qctrlcommons.exceptions import QctrlGqlException
from qctrlcommons.serializers import DataTypeDecoder
from tqdm.auto import tqdm

from .result_mixin import ResultMixin
from .utils import _get_function_name


class AsyncResult:
    """
    Handles refreshing the action result and reporting progress.
    """

    def __init__(
        self,
        gql_client: Client,
        action: ResultMixin,
        progress_bar: tqdm,
        refresh_query: DocumentNode,
    ):
        self.gql_client = gql_client
        self.action = action
        self.progress = progress_bar
        self.refresh_query = refresh_query
        self._seen = set()

    def _get_message(self) -> Optional[str]:
        if self.action.status == self.action.PENDING:
            return (
                f"Your task {_get_function_name(self.action.name)} is currently in "
                "a queue waiting to be processed."
            )
        if self.action.status == self.action.STARTED:
            return f"Your task {_get_function_name(self.action.name)} has started."
        if self.action.status == self.action.SUCCESS:
            return (
                f"Your task {_get_function_name(self.action.name)} has completed "
                f"in {ceil(self.progress.format_dict['elapsed'])}s."
            )
        return None

    def refresh(self) -> Dict:
        """
        refresh the result and report the remaining tasks in the queue.


        Returns
        -------
        Dict
            query result related to action object.

        Raises
        ------
        QctrlGqlException
            if there are some errors in `coreAction` query.
        """
        query_result: Dict = self.gql_client.execute(self.refresh_query)

        if query_result["coreAction"].get("errors"):
            raise QctrlGqlException(
                query_result["coreAction"].get("errors"), format_to_snake=True
            )
        result = query_result["coreAction"]["coreAction"]

        if result["action"].get("result") is not None:
            action_result = json.loads(
                result["action"].pop("result"), cls=DataTypeDecoder
            )
            result.update(action_result)

        return result

    def write_waiting_message(self) -> None:
        """
        Displays a message for the current status if that message has not already been seen.

        Should be called after the `action` has been updated with the result of `refresh`.
        """
        message = self._get_message()
        if message and message not in self._seen:
            self.progress.write(message)
            self._seen.add(message)
