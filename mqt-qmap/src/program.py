"""MQT QMAP as a Service"""

from __future__ import annotations

import ast
import time
from typing import Any

from loguru import logger
from mqt.qmap import Architecture, compile
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
    qc_qasm: str | None = data.get("qc")
    if qc_qasm is None:
        return ErrorResponse(code="400", detail="No input circuit provided.")

    arch_num_qubits: int | None = data.get("arch_num_qubits")
    if arch_num_qubits is None:
        return ErrorResponse(code="400", detail="Number of qubits for architecture missing.")

    arch_coupling_map: str | None = data.get("arch_coupling_map")
    if arch_coupling_map is None:
        return ErrorResponse(code="400", detail="Coupling map for architecture missing.")

    coupling_map: set[tuple[int, int]] = ast.literal_eval(arch_coupling_map)
    arch = Architecture(arch_num_qubits, coupling_map)

    # Configuration options for the mapper
    method = params.get("method", "heuristic")

    qc = loads(qc_qasm)

    logger.info("Starting execution...")
    start_time = time.time()
    _, results = compile(circ=qc, arch=arch, method=method)
    execution_time = time.time() - start_time
    logger.info("Finished execution")

    result = {
        "qc_mapped": results.mapped_circuit,
    }
    metadata = {
        "qmap_results": results.json(),
        "execution_time": round(execution_time, 4),
    }
    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
