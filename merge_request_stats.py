"""TODO."""
import functools
import json
import logging
import os
import warnings
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

import gitlab
import requests
from gitlab.base import RESTObjectList
from gitlab.v4.objects.groups import Group


def silence_urllib3_warnings(func):  # type: ignore
    """Decorator to silence urllib3 warning messages."""

    @functools.wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> requests.Response:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            return func(*args, **kwargs)

    return wrapper


class MergeRequestStats:
    """Everything related to fetching merge request statistics for a gitlab group."""

    @silence_urllib3_warnings
    def __init__(
        self,
        url: str,
        token: str,
        group: str,
        ssl_verify: bool = False,
    ) -> None:
        """Constructor.

        :param url: the gitlab server url
        :param token: the gitlab token to authenticate with
        :param group: the gitlab group to work with
        :param ssl_verify: enable/disable ssl verification
        """
        self.git_lab: gitlab.Gitlab = gitlab.Gitlab(
            url=url,
            private_token=token,
            ssl_verify=ssl_verify,
        )

        self.group: Group = self.git_lab.groups.get(group)
        self.authors: Dict[str, Any] = {}

    @silence_urllib3_warnings
    def get_merge_requests(self) -> RESTObjectList:
        """Gets merge requests for the group (iterator by default)."""
        return self.group.mergerequests.list(iterator=True)

    @silence_urllib3_warnings
    def calculate(self) -> None:
        """Calculates statistics for the group.

        Does the following:
            1. Checks MR's for the past 7 days
            2. Gets total counts of MR's per author and identifies which repos they were into
        """
        time_now = datetime.now()

        for merge_request in self.get_merge_requests():
            created_date = datetime.strptime(
                merge_request.created_at,
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            time_delta = time_now - created_date
            if abs(time_delta.days) > 7:
                break

            username: str = merge_request.author["username"]

            if username not in self.authors:
                self.authors[username] = {
                    "name": merge_request.author["name"],
                    "total": 0,
                    "projects": {},
                }

            self.authors[username]["total"] += 1

            project_name: str = merge_request.references["full"].split("!")[0]
            if project_name not in self.authors[username]["projects"]:
                self.authors[username]["projects"][project_name] = 0

            self.authors[username]["projects"][project_name] += 1

        print(json.dumps(self.authors, indent=4))


if __name__ == "__main__":
    merge_request_stats: MergeRequestStats = MergeRequestStats(
        os.getenv("GITLAB_URL"),
        os.getenv("GITLAB_API_ACCESS_TOKEN"),
        os.getenv("GITLAB_GROUP"),
    )
    merge_request_stats.calculate()
