from __future__ import annotations

import json
from typing import Any


class Response:
    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: getattr(o, "__dict__", str(o)), sort_keys=False)


class ErrorResponse(Response):
    """
    Represents an error to be passed back to the caller.

    Args:
        code (str): application-specific code representing the type of problem encountered
        detail (str): application-specific error message describing the detail of the problem encountered
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail


class ResultResponse(Response):
    """
    Represents the result to be passed back to the caller.

    Args:
        result (dict): application-specific result to be passed back to the caller; must be JSON serializable
    """

    def __init__(self, result: dict, metadata: dict[str, Any] | None = None) -> None:
        self.result = result
        self.metadata = metadata
