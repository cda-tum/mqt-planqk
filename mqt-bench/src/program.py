"""MQT Bench as a Service"""

from __future__ import annotations

import time
from typing import Any

from loguru import logger
from mqt.bench import get_benchmark
from qiskit.qasm2 import dumps

from .libs.return_objects import ErrorResponse, ResultResponse


def run(_data: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> ResultResponse | ErrorResponse:
    """Default entry point.

    Parameters:
        _data: The input data sent by the client
        params: Contains parameters, which can be set by the client to configure the execution.

    Returns:
        response: Response as arbitrary json-serializable dict or an error to be passed back to the client.
    """
    benchmark_name: str | None = params.get("benchmark_name")
    if benchmark_name is None:
        return ErrorResponse(code="400", detail="No benchmark name provided.")

    circuit_size: int | None = params.get("circuit_size")
    if circuit_size is None and benchmark_name not in {"groundstate", "shor"}:
        return ErrorResponse(code="400", detail="No circuit size provided.")

    benchmark_instance_name: str | None = params.get("benchmark_instance_name")
    if benchmark_instance_name is None and benchmark_name in {"groundstate", "shor"}:
        return ErrorResponse(code="400", detail="No benchmark instance name provided.")

    logger.info("Starting execution...")
    start_time = time.time()
    qc = get_benchmark(
        benchmark_name=benchmark_name,
        circuit_size=circuit_size,
        benchmark_instance_name=benchmark_instance_name,
        level=0,
    )
    execution_time = time.time() - start_time
    logger.info("Finished execution")

    result = {
        "qc": dumps(qc),
    }
    metadata = {
        "execution_time": round(execution_time, 4),
    }
    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
