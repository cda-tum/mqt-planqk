"""MQT QCEC as a Service"""

from __future__ import annotations

import time
from typing import Any

from loguru import logger
from mqt.qcec import verify
from qiskit.qasm3 import loads

from .libs.return_objects import ErrorResponse, ResultResponse


def run(data: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> ResultResponse | ErrorResponse:
    """Default entry point.

    Parameters:
        data: The input data sent by the client
        params: Contains parameters, which can be set by the client to configure the execution.

    Returns:
        response: Response as arbitrary json-serializable dict or an error to be passed back to the client.
    """
    qc1_qasm: str | None = data.get("qc1")
    if qc1_qasm is None:
        return ErrorResponse(code="400", detail="No first circuit provided.")

    qc2_qasm: str | None = data.get("qc2")
    if qc2_qasm is None:
        return ErrorResponse(code="400", detail="No second circuit provided.")

    # Configuration options for the equivalence checking manager.
    parallel = params.get("parallel", True)
    run_alternating_checker = params.get("run_alternating_checker", True)
    run_construction_checker = params.get("run_construction_checker", False)
    run_simulation_checker = params.get("run_simulation_checker", True)
    run_zx_checker = params.get("run_zx_checker", True)
    timeout = params.get("timeout", 3600.0)

    qc1 = loads(qc1_qasm)
    qc2 = loads(qc2_qasm)

    logger.info("Starting execution...")
    start_time = time.time()
    results = verify(
        qc1,
        qc2,
        parallel=parallel,
        run_alternating_checker=run_alternating_checker,
        run_construction_checker=run_construction_checker,
        run_simulation_checker=run_simulation_checker,
        run_zx_checker=run_zx_checker,
        timeout=timeout,
    )
    execution_time = time.time() - start_time
    logger.info("Finished execution")

    result = {
        "equivalence": results.equivalence,
    }
    metadata = {
        "qcec_results": results.json(),
        "execution_time": round(execution_time, 4),
    }
    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
